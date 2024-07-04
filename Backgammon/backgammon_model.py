# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    03/07/2024
# Purpose: Implements Backgammon for the purposes of developing an AI
#          agent for ME344: Introduction to building High Performance
#          Computing clusters, at Stanford Summer Session 2024.

# IMPORTS ------------------------------------------------------------ #

from ExtendedFormGame.template import GameState, GameRules, Action

# CONSTANTS ---------------------------------------------------------- #

# CLASS DEF ---------------------------------------------------------- #

class BackgammonState(GameState):
    
    def __init__(self, num_agents, agent_id):
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


class BackgammonRules(GameRules):
    pass

class BackgammonAction(Action):
    pass


# END ---------------------------------------------------------------- #