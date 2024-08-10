# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan.
# Date:    24/07/2024
# Purpose: Implements Q-function for an Agent.

# IMPORTS ------------------------------------------------------------ #

from ExtendedFormGame.template import GameState
import ExtendedFormGame.utils as utils
import random

# CONSTANTS ---------------------------------------------------------- #

LEARNING_RATE:float = 0.1

# CLASS DEF ---------------------------------------------------------- #       

class QFunction():

    def __init__(self, alpha=LEARNING_RATE):
        # Initialise Q-function.
        self.alpha = alpha
    
    def get_q_value(self, game_game_state:GameState,
                    action:tuple) -> float:
        """ get_q_value
        Return Q-value for action,game_state pair.

        Args:
            game_game_state (GameState): State s
            action (Action): Action a
        
        Returns:
            float: Q-value
        """
        utils.raiseNotDefined()
        return 0
    
    def get_max_q(self, game_state:GameState,
                  actions:list[tuple]) -> float:
        """get_max_q
        Return the maximum Q-value from the actions.

        Args:
            actions (list[tuple]): List of Action a.
            game_state (GameState): State s.
        
        Returns:
            float: Maximum Q-value for the actions in state s.
        """
        # Initialise max variables.
        max_q = float("-inf")

        # Identify actions with max Q-value.
        for action in actions:
            tmp_q = self.get_q_value(game_state, action)
            if tmp_q > max_q:
                max_q = tmp_q
        
        return max_q
    
    def get_arg_max(self, game_state:GameState,
                  actions:list[tuple]) -> tuple:
        """Return the maximum Q-value from the actions.
    
        Args:
            actions (list[tuple]): List of Action a.
            game_state (GameState): State s.
        
        Returns:
            tuple: Action a that maximises the Q-value for game_state s.
        """
        # Initialise max variables.
        max_q = float("-inf")
        max_actions = None

        # Identify actions with max Q-value.
        for action in actions:
            tmp_q = self.get_q_value(game_state, action)
            if tmp_q > max_q:
                max_q = tmp_q
                max_actions = [action]
            elif tmp_q == max_q:
                max_actions.append(action)

        # Random tie-break of tied max values.
        return random.choice(max_actions)

    def update(self, game_state:GameState, game_state_p:GameState,
               actions_p:list[tuple], reward:float, gamma:float,
               agent_id:int) -> None:
        """update
        Updates the Q-value at a particular moment in the game.
    
        Args:
            game_state (GameState): State s
            game_state_p (GameState): State s'
            actions_p (list[tuple]): Actions in A'.
            reward (list[float]): List for the reward for each agent.
            gamma (float): Float for the gamma
            agent_id (int): Integer representing agent id.
        """
        utils.raiseNotDefined()
        return 0

    def save_policy(self, filename:str) -> None:
        """Saves a policy to a specific filename.
    
        Args:
            filename (str): String describing filepath and filename
            to save Q-function to.
        """
        utils.raiseNotDefined()
        return 0
    
    def load_policy(self, filename:str) -> None:
        """Load a policy from a specific filename.

        Args:
            filename (str): String describing filepath and filename
            to save Q-function to.
        """
        utils.raiseNotDefined()
        return 0

# END FILE ----------------------------------------------------------- #