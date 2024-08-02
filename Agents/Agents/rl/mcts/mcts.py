# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    29/07/2024
# Purpose: Implements an agent that uses MCTS learning.

# IMPORTS ------------------------------------------------------------ #

from datetime import datetime, timedelta
from Agents.rl.template.bandit import Bandit
from Agents.rl.template.mdp import MDP
from Agents.rl.template.qfunction import QFunction
from ExtendedFormGame import utils
from ExtendedFormGame.template import Agent, GameRules, GameState
from Agents.rl.mcts.multi_agent_node import MultiAgentNode

# CONSTANTS ---------------------------------------------------------- #

BUFFER_TIME:float = float(0.25)
FIRST_TURN_TIME:float = float(15.0)
SUBSEQUENT_TURN_TIME:float = float(1.0)
SIMULATION_DEPTH:int = int(3)

# CLASS DEF ---------------------------------------------------------- #  

class MCTSAgent(Agent):
    def __init__(self,_id: int, qfunction:QFunction,
                 game_rules:GameRules, mdp:MDP, bandit:Bandit) -> None:
        super().__init__(_id)
        self.game_rules:GameRules = game_rules
    
        # Define data structures to support MCTS.
        self.qfunction:QFunction = qfunction
        self.mdp:MDP = mdp
        self.bandit:Bandit = bandit
        self.turn:int = 0
        self.root_node:MultiAgentNode = None
        self.simulation_limit:int = SIMULATION_DEPTH


    def select_action(self, game_state:GameState,
                      actions:list[tuple]) -> tuple:
        """select_action
        Given a set of available actions for the agent to execute, and
        a copy of the current game state (including that of the agent),
        select one of the actions to execute.

        Args:
            game_state (GameState): Instance of GameState.
            actions (list[Action]): List of Action instances.

        Returns:
            Action: Selected action instance.
        """

        start:datetime = datetime.now()

        print("TURN "+str(self.turn)+" AGENT "+str(self.id))

        if self.turn == 0:
            # First turn: 15sec of execution - perform MCTS.
            fin = start + timedelta(seconds=(FIRST_TURN_TIME-BUFFER_TIME))   
        else:
            # Subsequent turn: 1sec oclef execution.
            fin = start + timedelta(seconds=(SUBSEQUENT_TURN_TIME-BUFFER_TIME))

        # Execute MCTS until finish time.
        timer_s = datetime.now()
        self._mcts(fin, game_state)
        timer_f = datetime.now()
        print("MCTS DURATION: "+str(timer_f - timer_s))  

        # Select next best action.
        timer_s = datetime.now()
        action = self.qfunction.get_arg_max(game_state, actions)
        timer_f = datetime.now()
        print("ACTION SELECTION DURATION: "+str(timer_f - timer_s))
        print()

        # Update turn.
        self.turn += 1
        self.root_node = None

        return action
    
    def heuristic(self, game_state:GameState,
                  action:tuple) -> float:
        """heuristic
        Return heuristic value for applying action a in game state s.
        This assumes that we are comparing actions in the same game
        state, therefore we have the same cost to reach that state.

        Args:
            game_state (GameState): Game state s.
            action (tuple): Action a.

        Returns:
            float: heuristic value
        """
        utils.raiseNotDefined
        return 0

    # MCTS ----------------------------------------------------------- #
    def _mcts(self, fin_time:datetime, game_state:GameState):
        """Execute the MCTS algorithm from the given initial state until
        the finish time is reached using Miller's (2023) approach.
    
        Reference List:
            Miller, T. (2023) Monte-Carlo Tree Search (MCTS). rl-notes.
            https://gibberblot.github.io/rl-notes/single-agent/mcts.html#

        Args:
            fin_time (DateTime): Finish time of execution loop.
            root_node (MultiAgentNode, optional): Root node. Defaults
            to None.
        """
        if self.root_node is None:
            # First turn: Create search tree from state s.
            self.root_node:MultiAgentNode = self._createRootNode(game_state)

        cur_time = datetime.now()
        while (cur_time < fin_time):
            # Find node to expand
            selected_node:MultiAgentNode = self.root_node.select()
            if not self.mdp.is_terminal_state(selected_node.agent_id,
                                              selected_node.game_state):
                # Expand and simulate
                child:MultiAgentNode = selected_node.expand(self.heuristic)
                reward:list = child.simulate([float(0.0),float(0.0)],
                                             int(0), self.heuristic)
                selected_node.backpropogate(reward, child)
            
            cur_time = datetime.now()
    
    def _createRootNode(self, game_state:GameState):
        """Create root node for MCTS.
        Args:
            state (GameState): State s.

        Returns:
            MultiAgentNode: Root node.
        """
        return MultiAgentNode(mdp=self.mdp,
                              parent=None,
                              state=game_state,
                              qfunction=self.qfunction,
                              bandit=self.bandit, agent_id=self.id, 
                              simulation_depth=self.simulation_limit)
    
    # I/O Helpers ---------------------------------------------------- #
    def update_endgame_weights(self, history:dict) -> None:
        """update_endstate_weights
        Updates the weights using the history printout for the match to
        accurately capture rewards at endgame state.

        Args:
            history (dict): Dictionary storing winning results and the
            history for the game.
        """
        # Do nothing - not a learning-based approach.
        return None
    
    def save_weights(self) -> None:
        """save_weights
        Save training weights for learning-based agents.
        """
        # Do nothing - not a learning-based approach.
        return None
    
# END ---------------------------------------------------------------- #