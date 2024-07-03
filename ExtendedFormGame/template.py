# INFORMATION -------------------------------------------------------- #

# Author:  Code leveraged from COMP90054 Assignment 3.
# Date:    03/07/2024
# Purpose: Implements template classes for game state, actions, game
#          rules, and agents.

# IMPORTS ------------------------------------------------------------ #

import utils
import random

# CONSTANTS ---------------------------------------------------------- #


# CLASS DEF ---------------------------------------------------------- #

class GameState():
    def __init__(self, num_agents, agent_id):
        pass

class Action():
    pass

class GameRule:
    def __init__(self, num_agents = 2):
        self.current_agent_index = 0
        self.num_agents = num_agents
        self.current_game_state = self.initial_game_state()
        self.action_counter = 0

    def initial_game_state(self):
        utils.raiseNotDefined()
        return 0

    def generate_successor(self, game_state, action, agent_id):
        utils.raiseNotDefined()
        return 0

    def get_next_agent_index(self):
        return (self.current_agent_index + 1) % self.num_of_agent

    def get_legal_actions(self, game_state, agent_id):
        utils.raiseNotDefined()
        return []

    def calculate_score(self, game_state,agent_id):
        utils.raiseNotDefined()
        return 0

    def game_ends(self):
        utils.raiseNotDefined()
        return False

    def update(self, action):
        temp_state = self.current_game_state
        self.current_game_state = self.generate_successor(temp_state,
                                                          action,
                                                          self.current_agent_index)
        self.current_agent_index = self.get_next_agent_index()
        self.action_counter += 1

    def getCurrentAgentIndex(self):
        return self.current_agent_index

# END ---------------------------------------------------------------- #