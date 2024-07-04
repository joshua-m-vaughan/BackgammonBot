# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging and extending code from COMP90054
#          Assignment 3.
# Date:    XX/XX/2024
# Purpose: Implements a Game class to run implemented games for this
#          sequential extended form game framework.

# IMPORTS ------------------------------------------------------------ #

import random
from template import Agent, GameRules

# CONSTANTS ---------------------------------------------------------- #

WARMUP = 10 # Warm-up period for each agent on their first turn.

# CLASS DEF ---------------------------------------------------------- #

class Game():

    def __init__(self, GameRules:GameRules, agent_list:Agent,
                 agent_names:list[str], num_agents:int,
                 seed:int = 1, time_limit:int = 1,
                 warning_limit:int = 3) -> None:
        """__init__
        Initialise an instance of Game class.

        Args:
            GameRules (GameRules): Instance of GameRules, specifying
            the rules of the game.
            agent_list ([Agent]): List of Agent instances.
            agent_names ([str]): List of strings for each agent's name.
            num_agents (int): Number of agents in the game.
            seed (int, optional): Random seed. Defaults to 1.
            time_limit (int, optional): Turn time limit. Defaults to 1.
            warning_limit (int, optional): Number of warnings for
            exceeding time limit. Defaults to 3.
        """
        
        # Instantiate the random library with seed for repeatability.
        self.seed = seed
        random.seed(self.seed)

        # Ensure that valid game is being formed.
        i = 0
        for player in agent_list:
            assert(player.id == i)
            i += 1

        self.game_rule = GameRules(num_agents)
        self.agents = agent_list
        self.agents_names = agent_names
        self.num_agents = num_agents
        self.time_limit = time_limit
        self.warning_limit = warning_limit
        self.warnings = [0]*num_agents
        self.warning_positions = []

    def run(self) -> None:
        """run
        This method runs a game until the termination state of the game
        is achieved.    
        """
        return None

    def _end_game(self, history:dict, is_time_out:bool = False,
                  time_out_id:int = None) -> None:
        """_end_game
        Private method completes the end game writing of the game state
        at the termination state of the game.

        Args:
            history (dict): Dictionary capturing the state of the game.
            is_time_out (bool, optional): Boolean indicating if game was
            terminated due to a time-out or an agent winning. Defaults
            to False.
            time_out_id (int, optional): Integer of timed out agent.
            Defaults to None.
        """
        return None
        
        

# END ---------------------------------------------------------------- #