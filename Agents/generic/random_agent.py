# INFORMATION ------------------------------------------------------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    21/07/2024
# Purpose: Implements a Random agent for a generic board game.

# IMPORTS ------------------------------------------------------------------------------------------------------------#

from ExtendedFormGame.template import Agent, GameState
import random

# CONSTANTS ----------------------------------------------------------------------------------------------------------#


# CLASS DEF ----------------------------------------------------------------------------------------------------------#  

class myAgent(Agent):
    def __init__(self,_id: int) -> None:
        super().__init__(_id)
    
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
        return random.choice(actions)
    
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