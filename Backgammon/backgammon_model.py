# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    03/07/2024
# Purpose: Implements Backgammon for the purposes of developing an AI
#          agent for ME344: Introduction to building High Performance
#          Computing clusters, at Stanford Summer Session 2024.

# IMPORTS ------------------------------------------------------------ #

import random
from ExtendedFormGame.template import GameState, GameRules, Action

# CONSTANTS ---------------------------------------------------------- #

MIN_DICE_VALUE = 1
MAX_DICE_VALUE = 6
NUM_BACKGAMMON_AGENTS = 2
STARTING_AGENT_ID = 0

# CLASS DEF ---------------------------------------------------------- #

class BackgammonState(GameState):
    
    def __init__(self,
                 num_agents=NUM_BACKGAMMON_AGENTS,
                 agent_id = STARTING_AGENT_ID):
        """__init__
        Initialise an instance of BackgammonState class.

        Args:
            num_agents (int, optional): Number of agents in the game.
            Defaults to 2.
            STARTING_AGENT_ID (int, optional): Starting Agent ID.
            Defaults to 0.

        """
        # Assert expected input from Game builder.
        assert (num_agents == 2)
        assert (agent_id == 0)

        # Initialise GameState attributes.
        self.num_agents = num_agents
        self.current_agent_id = agent_id

        # Initialise the board state attributes.
        self.points_content = [0] * 25
        self.black_checkers = [0]
        self.white_checkers = [0]
        self.black_checkers_taken = 0
        self.white_checkers_taken = 0

        # Initialise the dice attributes.
        self.dice = [0, 0]
    
    def roll(self):
        """roll
        Roll the dice to generate a new set of two dice representation.
        """

        for i in len(self.dice):
            self.dice = random.randrange(MIN_DICE_VALUE, MAX_DICE_VALUE)
        
        return None


class BackgammonRules(GameRules):
    pass

class BackgammonAction(Action):
    pass


# END ---------------------------------------------------------------- #