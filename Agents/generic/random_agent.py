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

class RandomAgent(Agent):
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
        print(actions)
        return random.choice(actions)
    
# END ---------------------------------------------------------------- #