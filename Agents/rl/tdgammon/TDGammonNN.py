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

TD_ALPHA:float = 0.7 # As defined in Tesauro paper.
NUM_TDGAMMON_FEATURES:int = 198 # As defined, by Tesauro's paper.
NUM_TDGAMMON1_HIDDEN:int = 40 # As defined, by Tesauro's paper.
NUM_TDGAMMON_OUTPUT:int = 1 # As defined, by Tesauro's paper.

# CLASS DEF ---------------------------------------------------------- #      

class NNQFunction(QFunction):

    def __init__(self, alpha = TD_ALPHA) -> None:
        
        super().__init__(alpha)
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

class TDGammonNN(nn.Module):
    
    def __init__(self, num_hidden_units:int = NUM_TDGAMMON1_HIDDEN):
        super().__init__()

        # Define our hidden layer.
        self.hidden = nn.Sequential(
            nn.Linear(in_features=NUM_TDGAMMON_FEATURES,
                      out_features=num_hidden_units),
            nn.Sigmoid()
        )

        # Define the output layer.
        self.output = nn.Sequential(
            nn.Linear(in_features=num_hidden_units,
                      out_features=NUM_TDGAMMON_OUTPUT),
            nn.Sigmoid()
        )

        # Initialise weights to zero.
        for p in self.parameters():
            nn.init.zeros_(p)
    
    # NOTE: Overriding method.
    def forward(self, x):
        """forward
        Model inference.

        Args:
            x (list[float]): A list of floats.
        """
        x = torch.from_numpy(np.array(x))
        x = self.hidden(x)
        x = self.output(x)
        return x

# END FILE ----------------------------------------------------------- #