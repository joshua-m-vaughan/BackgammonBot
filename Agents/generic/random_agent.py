# INFORMATION ------------------------------------------------------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    21/07/2024
# Purpose: Implements a Random agent for a generic board game.

# IMPORTS ------------------------------------------------------------------------------------------------------------#

from ExtendedFormGame.template import Agent
import random

# CONSTANTS ----------------------------------------------------------------------------------------------------------#


# CLASS DEF ----------------------------------------------------------------------------------------------------------#  

class RandomAgent(Agent):
    def __init__(self,_id: int) -> None:
        super().__init__(_id)
    
    def SelectAction(self,actions,game_state):
        return random.choice(actions)
    
# END ---------------------------------------------------------------- #