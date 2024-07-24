# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, extending Node definition outlined in Tim
#          Miller's online resource.
# Date:    24/07/2024
# Purpose: Implements Nodes for multi-agent MCTS.

# Reference List:
#   - Miller, T. (2023) Monte-Carlo Tree Search (MCTS). rl-notes.
#     https://gibberblot.github.io/rl-notes/single-agent/mcts.html#

# IMPORTS ------------------------------------------------------------ #

from collections import defaultdict
from operator import add
from copy import deepcopy

from Agents.rl import Bandit
from Agents.rl.mdp import MDP
from Agents.rl.qfunction import QFunction
from ExtendedFormGame import utils
from ExtendedFormGame.template import GameState

# CONSTANTS ---------------------------------------------------------- #       

SIMULATION_LIMIT:int = 3

# CLASS DEF ---------------------------------------------------------- #       

class MultiAgentNode():
    
    # Implement variables for tracking instances.
    next_node_id:int = 0
    visits:dict = defaultdict(lambda: 0)

    def __init__(self, mdp:MDP, parent, game_state:GameState,
                 qfunction:QFunction, bandit:Bandit, agent_id:int,
                 reward:list[float] =[float(0.0), float(0.0)],
                 action:tuple = None) -> None:
        self.mdp:MDP = mdp
        self.parent = parent
        self.children:dict = defaultdict(lambda: [])
        self.game_state:GameState = game_state
        self.id:int = MultiAgentNode.next_node_id
        MultiAgentNode.next_node_id += 1

        # Q-function to store q-values.
        self.qfunction:QFunction = qfunction

        # Multi-armed bandit.
        self.bandit:Bandit = bandit
        self.agent_id:int = agent_id

        # The immediate reward received for reaching this game_state,
        # used for backpropagation.
        # TECH DEBT: Hard coding two-player limitations here.
        self.reward:list[float] = reward

        # The action that generated this node
        self.action:tuple = action

    def select(self):
        """Select a branch in the tree using multi-armed bandit
        strategy, and return the child node to be expanded, using
        Miller's (2023) approach.

        Reference List:
            Miller, T. (2023) Monte-Carlo Tree Search (MCTS). rl-notes.
            https://gibberblot.github.io/rl-notes/single-agent/mcts.html#

        Returns:
            MultiAgentNode: Node representing the next node to select
            for expansion.
        """
        if (not self._isFullyExpanded()
            or self.mdp.is_terminal_state(self.game_state, self.agent_id)):
            # Reached a leaf node, or no further to expand to.
            return self
        else:
            # Select next node to expand using n-bandit strategy.
            actions:list[tuple] = []
            for (_, value) in self.children.items():
                for (_, action) in value:
                    actions.append(action)
            action:tuple = self.bandit.select_action(self.game_state, actions)
            new_node = self.get_outcome_child(action).select()
            return new_node

    def _isFullyExpanded(self):
        actions:list[tuple] = self.mdp.get_actions(self.game_state,
                                                   self.agent_id)
        if len(actions) == len(self.children.keys()):
            return True
        else:
            return False

    def get_outcome_child(self, action:tuple):
        """ Get next game_state and return the child node using Miller's
        (2023) approach, but modified to account for a multi-agent turn
        based game.

        Reference List:
            Miller, T. (2023) Monte-Carlo Tree Search (MCTS). rl-notes.
            https://gibberblot.github.io/rl-notes/single-agent/mcts.html#

        Args:
            action (tuple): Action a.

        Returns:
            MultiAgentNode: Child node.
        """
        # Generate next game_state and reward for achieving that game_state.
        next_game_state:GameState = self.mdp.get_next_state(deepcopy(self.game_state),
                                                            action, self.agent_id)
        reward:list[float] = [float(0.0), float(0.0)] # TECH DEBT: Hard coding two-player limitations here.
        reward[self.agent_id] = self.mdp.get_reward(self.game_state,
                                                    next_game_state,
                                                    action,
                                                    self.agent_id)
        
        # Validate if this game_state is already a child game_state.
        if str(action) in list(self.children.keys()):
            for (child,_) in self.children[str(action)]:
                if next_game_state == child.game_state:
                    return child
                    
        # Create a new node for new child
        next_agent_id = 1 if self.agent_id == 0 else 0
        new_child = MultiAgentNode(self.mdp, self, deepcopy(next_game_state),
                                   self.qfunction, self.bandit, next_agent_id,
                                   reward, action)
        # Add child node into parent's list of children.
        self.children[str(action)].append((new_child, action))
        return new_child

    def expand(self):
        """Expand a multi-agent node, on the basis that it has not been
        expanded yet using Miller's (2023) approach.

        Reference List:
            Miller, T. (2023) Monte-Carlo Tree Search (MCTS). rl-notes.
            https://gibberblot.github.io/rl-notes/single-agent/mcts.html#

        Returns:
            MultiAgentNode: Node representing the next node to simulate from.
        """
        if not self.mdp.is_terminal_state(self.game_state, self.agent_id):
            # Select next action to expand.
            actions = self.mdp.get_actions(self.game_state, self.agent_id)
            action = self._heuristicSelect(actions)
            self.children[str(action)] = []
            return self.get_outcome_child(action)
        else:
            # In terminal game_state: no further to expand.
            return self

    def _heuristicSelect(self, actions):
        """Select next action using a heuristic.

        Returns:
            Action: Action a.
        """
        utils.raiseNotDefined()
        return 0

    def backpropogate(self, reward, child):
        """Backpropogate the reward from the terminal game_state back to the
        root node using Miller's (2023) approach.

        Reference List:
            Miller, T. (2023) Monte-Carlo Tree Search (MCTS). rl-notes.
            https://gibberblot.github.io/rl-notes/single-agent/mcts.html#
        """

        action = child.action

        # Update visit counter.
        MultiAgentNode.visits[self.game_state] += 1
        MultiAgentNode.visits[(action, self.game_state)] += 1
        
        # Update Q-function.
        delta = ((1 / (MultiAgentNode.visits[(action, self.game_state)]))
                 * (reward[self.agent_id]
                    -self.qfunction.get_q_value(self.game_state, action)))
        self.qfunction.update(self.game_state, action, delta)

        # Recursive call unless reached root node.
        if self.parent is not None:
            self.parent.backpropogate(tuple(map(add, self.reward, reward)),
                                      self)
    
    def simulate(self, cum_reward, depth):
        """ Simulate a game from a node to a terminal game_state
        using Miller's (2023) approach that stores subsequent search nodes.
    
        Reference List:
            Miller, T. (2023) Monte-Carlo Tree Search (MCTS). rl-notes.
            https://gibberblot.github.io/rl-notes/single-agent/mcts.html#
        
        Args:
            node (MultiAgentNode): Node to be simulated from.

        Returns:
            [float, float]: Cumulative reward for simulation from node.
            TECH DEBT: Hard coded for a two-player game here.
        """

        if (not self.mdp.is_terminal_state(self.game_state, self.agent_id)
            and sum(depth) < SIMULATION_LIMIT):
            # Select an action using heuristic.
            actions = self.mdp.get_actions(self.game_state, self.agent_id)
            action = self._heuristicSelect(actions)
            # Execute the action, and get the child node.
            child = self.get_outcome_child(action)

            # Discount the reward for the agent.
            parent_id = 1 if self.agent_id == 0 else 0
            cum_reward[parent_id] += (pow(self.mdp.gamma, depth[parent_id])
                                          * self.reward[parent_id])
            depth[self.agent_id] += 1

            # Simulate from next node.
            return child.simulate(cum_reward, depth)
        else:
            return cum_reward
        
# END FILE ------------------------------------------------------------ #