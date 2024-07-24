# INFORMATION ------------------------------------------------------------------------------------------------------- #

# Author:  Josh Vaughan, utilising codebase provided in Tim Miller's RL online textbook.
# Date:    24/07/2024
# Purpose: Implements Bandit for the Splendor game.

# Reference List:
#   - Miller, T. (2023) Multi-armed Bandits. rl-notes.
#     https://gibberblot.github.io/rl-notes/single-agent/multi-armed-bandits.html

# IMPORTS ------------------------------------------------------------------------------------------------------------#

from Agents.rl.qfunction import QFunction
from ExtendedFormGame.template import Agent, GameState
import random
import math
import ExtendedFormGame.utils as utils
from collections import defaultdict

# IMPORTS ------------------------------------------------------------------------------------------------------------#

DEFAULT_COUNT = int(0)
PRIMED_COUNT = int(1)
DEFAULT_EXPLORE = float(1)
DEFAULT_EPSILON = float(0.5)

# CLASS DEF ----------------------------------------------------------------------------------------------------------#       

class Bandit(Agent):
    def __init__(self,_id: int, qfunction:QFunction) -> None:
        super().__init__(_id)
        
        # Store Q-function for the Bandit and control QFunction access
        # through bandit.
        self.qfunction = qfunction
    
    def select_action(self, game_state:GameState,
                      actions:list[tuple]) -> tuple:
        """Return the action selected according the Bandit's strategy.

        Args:
            game_state (GameState): State s.
            actions (list[tuple]): A list of actions.
        
        Returns:
            tuple: The action according the Bandit's strategy.
        """
        utils.raiseNotDefined()
        return 0

class UCBOneBandit(Bandit):
    """Implementation of the UCB1-strategy for a Multi-armed bandit
    using Miller's (2023) approach.

    Reference List:
        Miller, T. (2023) Multi-armed Bandits. rl-notes.
        https://gibberblot.github.io/rl-notes/single-agent/multi-armed-bandits.html
    """

    def __init__(self, _id, qfunction, default_count=DEFAULT_COUNT):
        super().__init__(_id, qfunction)
        
        # Include counters for updates.
        self.total = 0
        self.times_selected = defaultdict(lambda: default_count)

    def select_action(self, game_state:GameState,
                      actions:list[tuple]) -> tuple:
        """Return the action selected according the Bandit's strategy.

        Args:
            game_state (GameState): State s.
            actions (list[tuple]): A list of actions.
        
        Returns:
            tuple: The action according the Bandit's strategy.
        """
        # Ensure that each action has been marked as executed once to
        # prevent undefined selection.
        for action in actions:
            if str(action) not in self.times_selected.keys():
                # Mark as selected.
                self.times_selected[str(action)] = 1
                self.total += 1
                return action
        
        # Argmax action for UCB1 approach.
        max_actions = []
        max_value = float("-inf")
        for action in actions:
            value = (self.qfunction.get_q_value(game_state, action)
                        + math.sqrt(
                        2 * math.log(self.total)
                        / self.times_selected[str(action)]
                        ))
            if value > max_value:
                max_value = value
                max_actions = [action]
            elif value == max_value:
                max_actions.append(action)
        
        # Random selection for tie-breaking.
        result = random.choice(max_actions)
        self.times_selected[result] += 1
        self.total += 1
        return result
    
    def __str__(self):
            return "UCBOne"

class SoftMaxBandit(Bandit):
    """Implementation of the SoftMax-strategy for a Multi-armed bandit
    using Miller's (2023) approach.
    
    Reference List:
        Miller, T. (2023) Multi-armed Bandits. rl-notes.
        https://gibberblot.github.io/rl-notes/single-agent/multi-armed-bandits.html
    """

    def __init__(self, _id, qfunction, tau=float(1.0)):
        super().__init__(_id, qfunction)
        self.tau = tau

    def select_action(self, game_state:GameState,
                      actions:list[tuple]) -> tuple:
        """Return the action selected according the Bandit's strategy.

        Args:
            game_state (GameState): State s.
            actions (list[tuple]): A list of actions.
        
        Returns:
            tuple: The action according the Bandit's strategy.
        """
        # Calculate the denominator of the SoftMax function. 
        denominator = float(0.0)
        for action in actions:
            denominator += math.exp(self.qfunction.get_q_value(game_state, action)/ self.tau)
        
        rand = random.random()
        cumulative_probability = float(0.0)
        result = None
        for action in actions:
            probability = (math.exp(self.qfunction.get_q_value(game_state, action)
                                    / self.tau)
                           / denominator)
            # Draw from Boltzmann distribution.
            if cumulative_probability <= rand <= cumulative_probability + probability:
                result = action
            # Update cumulative probability.
            cumulative_probability += probability

        return result
    
    def __str__(self):
            return "SoftMax"
    
class UCT(Bandit):
    """Implementation of the UCB1-strategy for a Multi-armed bandit
    in a MCTS using Miller's (2023) approach.

    Reference List:
        Miller, T. (2023) Multi-armed Bandits. rl-notes.
        https://gibberblot.github.io/rl-notes/single-agent/multi-armed-bandits.html
    """

    def __init__(self, _id, qfunction, explore = DEFAULT_EXPLORE, default_count=PRIMED_COUNT):
        super().__init__(_id, qfunction)
        
        # Include counters for updates.
        self.times_selected = defaultdict(lambda: default_count)
        self.explore = explore

    def select_action(self, game_state:GameState,
                      actions:list[tuple]) -> tuple:
        """Return the action selected according the Bandit's strategy.

        Args:
            game_state (GameState): State s.
            actions (list[tuple]): A list of actions.
        
        Returns:
            tuple: The action according the Bandit's strategy.
        """
        # Initialise variables.
        max_actions = []
        max_value = float("-inf")

        # Argmax action for UCB1 approach.
        for action in actions:
            value = (self.qfunction.get_q_value(game_state, action)
                        + (2 * self.explore 
                        * (math.sqrt((2
                                        * math.log(self.times_selected[str(game_state)]))
                                        / self.times_selected[(str(action), str(game_state))]
                                        )
                            )
                        )
                    )
            if value > max_value:
                max_value = value
                max_actions = [action]
            elif value == max_value:
                max_actions.append(action)
        
        # Random selection for tie-breaking.
        result = random.choice(max_actions)
        self.times_selected[(str(result), str(game_state))] += 1
        self.times_selected[str(game_state)] += 1
        return result
    
    def __str__(self):
            return "UCT"

class EpsilonGreedy(Bandit):
    """Implementation of the Epsilon greedy-strategy for a Multi-armed
    bandit using Miller's (2023) approach.

    Reference List:
        Miller, T. (2023) Multi-armed Bandits. rl-notes.
        https://gibberblot.github.io/rl-notes/single-agent/multi-armed-bandits.html
    """

    def __init__(self, _id, qfunction, epsilon = DEFAULT_EPSILON):
        super().__init__(_id, qfunction)
        self.epsilon = epsilon

    def select_action(self, game_state:GameState,
                      actions:list[tuple]) -> tuple:
        """Return the action selected according the Bandit's strategy.

        Args:
            game_state (GameState): State s.
            actions (list[tuple]): A list of actions.
        
        Returns:
            tuple: The action according the Bandit's strategy.
        """
        # Initialise variables.
        if random.random() < self.epsilon:
            return random.choice(actions)
        return self.qfunction.get_arg_max(game_state, actions)
    
    def __str__(self):
            return "UCT"

# END FILE -----------------------------------------------------------------------------------------------------------#
