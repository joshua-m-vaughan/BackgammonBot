# INFORMATION ------------------------------------------------------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    22/07/2024
# Purpose: Implements a running game agent for Backgammon.

# IMPORTS ------------------------------------------------------------------------------------------------------------#

from math import inf
from ExtendedFormGame.template import Agent, GameRules, GameState
import random

from backgammon_model import BackgammonRules

# CONSTANTS ----------------------------------------------------------------------------------------------------------#


# CLASS DEF ----------------------------------------------------------------------------------------------------------#  

class myAgent(Agent):
    def __init__(self,_id: int) -> None:
        super().__init__(_id)
        self.game_rules:GameRules = BackgammonRules() # TECH DEBT: Include this in agent specification.
    
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

        # Initialise heuristic values.
        max_h: float = -inf
        max_actions: list[tuple] = []

        # Access heuristic values.
        for action in actions:
            tmp_h = self.heuristic(game_state, action)
            if tmp_h > max_h:
                max_h = tmp_h
                max_actions = [action]
            elif tmp_h == max_h:
                max_actions.append(action)
        
        # Select heuristic maximising action
        return random.choice(max_actions)
    
    def heuristic(self, game_state:GameState,
                  action:tuple) -> float:
        """heuristic
        Return heuristic value for applying action a in game state s.
        This assumes that we are comparing actions in the same game
        state, therefore we have the same cost to reach that state.

        Args:
            game_state (GameState): Game state s.
            action (tuple): Action a.

        Returns:
            float: heuristic value
        """
        game_state_prime = self.game_rules.generate_successor(game_state,
                                                              action,
                                                              self.id)
        heuristic:float = (self.game_rules.calculate_score(game_state_prime, self.id)
                           - self.game_rules.calculate_score(game_state, self.id))
        return heuristic


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