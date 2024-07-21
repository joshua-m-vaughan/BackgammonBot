# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging and extending code from COMP90054
#          Assignment 3.
# Date:    XX/XX/2024
# Purpose: Implements a Game class to run implemented games for this
#          sequential extended form game framework.

# IMPORTS ------------------------------------------------------------ #

from copy import deepcopy
from func_timeout import func_timeout, FunctionTimedOut
import random
from ExtendedFormGame.template import Agent, GameRules, GameState

# CONSTANTS ---------------------------------------------------------- #

WARMUP = 10 # Warm-up period for each agent on their first turn.

# CLASS DEF ---------------------------------------------------------- #

class Game():

    def __init__(self, game_rules:GameRules, agent_list:Agent,
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

        self.game_rule = game_rules
        self.agents = agent_list
        self.agents_names = agent_names
        self.num_agents = num_agents
        self.time_limit = time_limit
        self.warning_limit = warning_limit
        self.warnings = [0]*num_agents
        self.warning_positions = []

    def run(self) -> dict:
        """run
        This method runs a game until the termination state of the game
        is achieved.    
        """

        history:dict = {"actions":[]}
        self.game_rule.action_counter = 0

        while not self.game_rule.game_ends(self.game_rule.current_game_state):
            
            # Current state of the game.
            agent_id:int = self.game_rule.current_agent_id
            assert (agent_id < self.num_agents)
            agent:Agent = self.agents[self.game_rule.current_agent_id]
            game_state:GameState = self.game_rule.current_game_state
            actions:tuple = self.game_rule.get_legal_actions(game_state,
                                                             self.game_rule.current_agent_id)
            gs_copy:GameState = deepcopy(game_state)
            actions_copy:tuple = deepcopy(actions)            

            # Agent selects action.
            timed_out:bool = False
            illegal_action:bool = False
            try: 
                selected:tuple = func_timeout(WARMUP if self.game_rule.action_counter < len(self.agents) else self.time_limit,
                                              agent.select_action,
                                              args=(gs_copy, actions_copy))
            except FunctionTimedOut:
                print( "Agent "+str(agent)+" timed out on action "+str(self.game_rule.action_counter)+".\n")
                selected = None
                timed_out = True

            # Evaluate if agent broke game rules in selecting an action.
            if agent_id != self.game_rule.num_agents:
                if not timed_out:
                    if selected not in actions:
                        illegal_action = True
            
            if timed_out or illegal_action:
                self.warnings[agent_id] += 1
                self.warning_positions.append((agent_id, self.game_rule.action_counter))
                selected = random.choice(actions)

            # Update game tracking, and the game state for the next
            # turn.
            history["actions"].append({self.game_rule.action_counter:
                                       {"agent_id":self.game_rule.current_agent_id,
                                        "action":selected}})
            self.game_rule.update(selected)

            print("Action: " + str(selected))

            # Early exit if there is an incorrect agent reference or warnings
            # are exceeded.
            if (self.warnings[agent_id] == self.warning_limit):
                    return (self._end_game(history,
                                           is_time_out=True,
                                           time_out_id=agent_id))
                
        # Score agent bonuses
        return (self._end_game(history, is_time_out=False))

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
        return history
        
        

# END ---------------------------------------------------------------- #