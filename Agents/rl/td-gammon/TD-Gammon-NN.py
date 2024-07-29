# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan
# Date:    XX/07/2024
# Purpose: Implements Neural Netowrk and QFunction using the
#          TD-Gammon 1.0 approach outlined by Tesauro's paper.

# Reference List:
#   Tesauro, G. (1995). Temporal difference learning and TD-Gammon.
#   Communications of the ACM, 38(3), 58-68.

# IMPORTS ------------------------------------------------------------ #

import numpy as np
import torch
import torch.nn as nn

from Agents.rl.template.qfunction import QFunction
from ExtendedFormGame import utils
from ExtendedFormGame.template import GameState

# CONSTANTS ---------------------------------------------------------- #

# CLASS DEF ---------------------------------------------------------- #      

class NNQFunction(QFunction):

    def __init__(self, alpha = None) -> None:
        
        # Create super class.
        if alpha is None:
            super().__init__()
        else:
            super().__init__(alpha)
        
        # Initialise subclass attributes.
        self.nn: TDGammonNN = None # TODO: Finish this implementation.
        
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

    def update(self, game_state:GameState, game_state_p:GameState,
               actions:list[tuple], reward:float, gamma:float,
               agent_id:int) -> None:
        """update
        Updates the Q-value at a particular moment in the game.
    
        Args:
            game_state (GameState): State s
            game_state_p (GameState): State s'
            action (Action): Action a
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

class TDGammonNN(torch.nn):
    pass

# END FILE ----------------------------------------------------------- #