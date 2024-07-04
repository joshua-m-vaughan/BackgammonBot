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
BLACK_ID = 0
WHITE_ID = 1
BLACK_HOME_POINT = 25
WHITE_HOME_POINT = 0

# CLASS DEF ---------------------------------------------------------- #

class BackgammonState(GameState):
    
    def __init__(self,
                 num_agents=NUM_BACKGAMMON_AGENTS,
                 agent_id = BLACK_ID):
        """__init__
        Initialise an instance of BackgammonState class.

        Args:
            num_agents (int, optional): Number of agents in the game.
            Defaults to 2.
            STARTING_AGENT_ID (int, optional): Starting Agent ID.
            Defaults to BLACK_ID.

        """
        # Assert expected input from Game builder.
        assert (num_agents == 2)
        assert (agent_id == 0)

        # Initialise GameState attributes.
        self.num_agents = num_agents
        self.current_agent_id = agent_id

        # Initialise the board state attributes.
        self.points_content = [0] * 26
        self.black_checkers = []
        self.white_checkers = []
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
    
    def __init__(self):
        """__init__
        Initialise an instance of GameRules class.
        """
        super.__init__(NUM_BACKGAMMON_AGENTS)

    def initial_game_state(self):
        """initial_game_state
        Returns the intial game state for the games rules.

        Returns:
            GameState: An instance of GameState class.
        """
        return BackgammonState(self.num_agents)
    
    def calculate_score(self, game_state, agent_id):
        """calculate_score
        Returns the pip score for agent ID in GameState s.

        Args:
            game_state (GameState): GameState s.
            agent_id (int): Agent ID.

        Returns:
            int: Integer representing the agent's score.
        """
        pip_score = 0
        if (agent_id == BLACK_ID):
            for point in game_state.black_checkers:
                pip_score += (game_state.points_content[point] *
                              abs(BLACK_HOME_POINT - point))
        elif (agent_id == WHITE_ID):
            for point in game_state.white_checkers:
                pip_score += (game_state.points_content[point] *
                              abs(WHITE_HOME_POINT - point))

        return pip_score

class BackgammonAction(Action):
    pass


# END ---------------------------------------------------------------- #