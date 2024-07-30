# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan
# Date:    29/07/2024
# Purpose: Implements Neural Netowrk and QFunction using the
#          TD-Gammon 1.0 approach outlined by Tesauro's paper.

# Reference List:
#   Tesauro, G. (1995). Temporal difference learning and TD-Gammon.
#   Communications of the ACM, 38(3), 58-68.

# IMPORTS ------------------------------------------------------------ #

from copy import deepcopy
import numpy as np
import torch
import torch.nn as nn

from Agents.rl.template.qfunction import QFunction
from backgammon_model import BackgammonState, generate_td_gammon_vector

# CONSTANTS ---------------------------------------------------------- #

TD_ALPHA:float = 0.7 # As defined in Tesauro paper.
TD_LAMDA:float = 0.01 # TO DETERMINE WHAT THIS IS.
NUM_TDGAMMON_FEATURES:int = 198 # As defined, by Tesauro's paper.
NUM_TDGAMMON1_HIDDEN:int = 40 # As defined, by Tesauro's paper.
NUM_TDGAMMON_OUTPUT:int = 1 # As defined, by Tesauro's paper.

# CLASS DEF ---------------------------------------------------------- #      

class TDGammonNNQFunction(QFunction):

    def __init__(self,
                 hidden_features:int = NUM_TDGAMMON1_HIDDEN,
                 alpha:float = TD_ALPHA,
                 lamda:float = TD_LAMDA) -> None:
        
        super().__init__(alpha)
        self.nn:TDGammonNN = TDGammonNN(hidden_features, lamda)
        
    def get_q_value(self, game_state:BackgammonState,
                    action:tuple) -> float:
        """ get_q_value
        Return Q-value for action,game_state pair.

        Args:
            game_state (GameState): State s
            action (Action): Action a
        
        Returns:
            float: Q-value
        """
        game_vector:np.array = generate_td_gammon_vector(game_state)
        return self.nn.forward(game_vector).detach().numpy()[0]
        # NOTE: THIS MIGHT NEED TO BE UPDATED TO REFLECT A SINGULAR FLOAT VALUE
        # FOR COMPARISON PURPOSES.

    def update(self, game_state:BackgammonState, game_state_p:BackgammonState,
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
        # Determine the delta.
        delta:float = (reward + (gamma *
                                 (self.get_q_value(game_state_p, None)
                                  - self.get_q_value(game_state, None))))
        
        # Update the weights.
        #NOTE: Improve efficiency by removing duplication of vectorisation.
        game_vec:np.array = generate_td_gammon_vector(game_state)
        self.nn.update_weights(self.nn.forward(game_vec),
                               self.alpha, gamma, delta[agent_id])


    def save_policy(self, filename:str) -> None:
        """Saves a policy to a specific filename.
    
        Args:
            filename (str): String describing filepath and filename
            to save Q-function to.
        """
        torch.save({"model_state_dict":self.nn.state_dict,
                    "eligbility": self.nn.eligibility_traces if self.nn.eligibility_traces else []},
                    f=filename+".pt")
        print("Model saved")
    
    def load_policy(self, filename:str) -> None:
        """Load a policy from a specific filename.

        Args:
            filename (str): String describing filepath and filename
            to save Q-function to.
        """
        checkpoint = torch.load(filename)
        self.nn.load_state_dict(checkpoint["model_state_dict"])
        self.nn.eligibility_traces = checkpoint["eligbility"]

class TDGammonNN(nn.Module):
    """TDGammonNN
    Implement a Neural Network class using PyTorch for TD-Gammon using
    the approach outlined by dellalibera on GitHub.

    Reference List:
        Della Libera A., td-gammon, (2019), Github repository,
        https://github.com/dellalibera/td-gammon
    """
    
    def __init__(self,
                 num_hidden_units:int = NUM_TDGAMMON1_HIDDEN, 
                 lamda:float = TD_LAMDA):
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

        # Initialise eligbility traces.
        self.lamda:float = lamda
        self.eligibility_traces:list = [torch.zeros(weights.shape, requires_grad=False) for weights in list(self.parameters())]
    
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
    
    def update_weights(self, output:torch.Tensor,
                       alpha:float,
                       gamma:float,
                       delta:float) -> None:
        """update_weights
        Update the weights of the model.

        Args:
            output (torch.Tensor): Output from training inference.
            alpha (float): Alpha value.
            gamma (float): Gamma value.
            delta (float): Delta value.
        """
        # Reset gradients.
        self.zero_grad()

        # Compute the derivative of the output w.r.t. the parameters.
        output.backward()

        with torch.no_grad():
            # Get parameters of the model.
            parameters = list(self.parameters())

            for i, weights in enumerate(parameters):
                # Compute eligbility traces:
                # e_t = (gamma * delta e_t-1) + (gradient of weights w.r.t. output)
                self.eligibility_traces[i] = (torch.Tensor((gamma * self.lamda * self.eligibility_traces[i]))
                                              + weights.grad)

                # Parameter Update:
                # theta <- theta + (alpha * delta * gradient of Q-function)
                new_weights = (weights +
                               (alpha * delta * self.eligibility_traces[i]))
                weights = deepcopy(new_weights)

# END FILE ----------------------------------------------------------- #