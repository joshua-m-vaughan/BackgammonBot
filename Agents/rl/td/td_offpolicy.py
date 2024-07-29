# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan.
# Date:    XX/07/2024
# Purpose: Implements an agent that uses Off-policy Temporal Difference
#          learning.

# IMPORTS ------------------------------------------------------------ #

from copy import deepcopy
import random

from Agents.rl.template.bandit import Bandit
from Agents.rl.template.mdp import MDP
from Agents.rl.template.qfunction import QFunction
from ExtendedFormGame.template import Agent, GameRules, GameState

# CONSTANTS ---------------------------------------------------------- #

# CLASS DEF ---------------------------------------------------------- #  

class OffPolicyTDAgent(Agent):
    def __init__(self,_id: int, qfunction:QFunction, game_rules:GameRules, mdp:MDP, bandit:Bandit) -> None:
        super().__init__(_id)
        self.game_rules:GameRules = game_rules
    
        # Define data structures to support off-policy TD learning.
        self.qfunction:QFunction = qfunction
        self.mdp:MDP = mdp
        self.bandit:Bandit = bandit
        self.turn:int = 0
        
        # Off-Policy TD variables.
        self.last_action: tuple = None
        self.last_state:GameState = None


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

        if self.last_action is None:
            # First action: randomly select an action.
            action:tuple = random.choice(actions)
        else:
            # Subsequent action: Bandit select next action.
            action:tuple = self.bandit.select_action(actions, game_state)

            # Observe reward
            reward:list[float] = self.mdp.get_reward(self.last_state,
                                                     game_state,
                                                     action,
                                                     self.id)
            
            # Update Q-function using off-policy approach.
            self.qfunction.update(self.last_state, game_state, actions,
                                  reward, self.mdp.gamma, self.id)

        # Update state, action storage for learning.
        self.last_action = deepcopy(action)
        self.last_state = deepcopy(game_state)

        # Update turn.
        self.turn += 1

        return action      

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