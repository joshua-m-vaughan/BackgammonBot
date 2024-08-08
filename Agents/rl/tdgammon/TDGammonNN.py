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
from pathlib import PurePosixPath, PureWindowsPath
import numpy as np
import torch
import torch.nn as nn

from Agents.rl.template.qfunction import QFunction
from BackgammonGame.backgammon_model import BackgammonRules, BackgammonState, generate_td_gammon_vector

# CONSTANTS ---------------------------------------------------------- #

TD_ALPHA:float = 0.01 # As defined in Tesauro paper.
TD_LAMDA:float = 0.70 # As defined in Tesauro paper.
NUM_TDGAMMON_FEATURES:int = 198 # As defined, by Tesauro's paper.
NUM_TDGAMMON1_HIDDEN:int = 40 # As defined, by Tesauro's paper.
NUM_TDGAMMON_OUTPUT:int = 2 # As defined, by Tesauro's paper. #HACK: This doesn't not include the gammon winning implementation which I haven't considered in the simulator.

# CLASS DEF ---------------------------------------------------------- #      

class TDGammonNNQFunction(QFunction):

    def __init__(self,
                 hidden_features:int = NUM_TDGAMMON1_HIDDEN,
                 alpha:float = TD_ALPHA,
                 lamda:float = TD_LAMDA) -> None:
        
        super().__init__(alpha)
        self.nn:TDGammonNN = TDGammonNN(hidden_features, lamda)
        self.gr:BackgammonRules = BackgammonRules()
        
    def get_q_value(self, game_state:BackgammonState,
                    action:tuple) -> torch.Tensor:
        """ get_q_value
        Return Q-value for action,game_state pair.

        Args:
            game_state (GameState): State s
            action (Action): Action a
        
        Returns:
            float: Q-value
        """
        if self.gr.game_ends(game_state):
            # NOTE: Game ends so we need to use exact result from
            # winning the game not the estimated value.
            output = np.zeros(self.gr.num_agents)
            for i in range(self.gr.num_agents):
                output[i] = self.gr.calculate_endgame_score(game_state, i)
        else:
            game_vector:np.array = generate_td_gammon_vector(game_state)
            output = self.nn.forward(game_vector).detach().numpy()
        return output

    def update(self, game_state:BackgammonState, game_state_p:BackgammonState,
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
        # Determine the delta.
        val = self.get_q_value(game_state, None)
        val_p = self.get_q_value(game_state_p, None)
        delta:float = (reward
                       + (gamma * val_p[agent_id])
                       - val[agent_id])
        
        # Update the weights.
        gs_vec = generate_td_gammon_vector(game_state)
        val_t = self.nn.forward(gs_vec)
        val_p_t = torch.Tensor(val_p)
        #val_p_t.requires_grad = True
        self.nn.update_weights(val_t, val_p_t,
                               self.alpha, gamma, delta)


    def save_policy(self, filepath:PureWindowsPath) -> None:
        """Saves a policy to a specific filename.
    
        Args:
            filepath (PureWindowsPath): String describing filepath and filename
            to save Q-function to.
        """
        filepath_str:str = str(PurePosixPath(filepath))
        torch.save({"model_state_dict":self.nn.state_dict(),
                    "eligbility": self.nn.eligibility_traces if self.nn.eligibility_traces else []},
                    f=filepath_str)
    
    def load_policy(self, filepath:PureWindowsPath) -> None:
        """Load a policy from a specific filename.

        Args:
            filepath (PureWindowsPath): String describing filepath and filename
            to save Q-function to.
        """
        filepath_str:str = str(PurePosixPath(filepath))
        checkpoint = torch.load(filepath_str)
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

        # Define loss function.
        self.loss = nn.MSELoss()

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
    
    def update_weights(self, prediction:torch.Tensor,
                       target:torch.Tensor,
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
        output = self.loss(prediction, target)
        output.backward()

        with torch.no_grad():
            # Get parameters of the model.
            parameters = list(self.parameters())

            for i, weights in enumerate(parameters):
                # Compute eligbility traces:
                # e_t = (gamma * delta e_t-1) + (gradient of weights w.r.t. output)
                # NOTE: I HAVE NOT BEEN ABLE TO UPDATE THE ETRACES AND
                # IN TURN THE WEIGHTS, BECAUSE THERE IS NEVER A GRADIENT
                # ON THE WEIGHTS. THE V_T+1 IS ALWAYS EQUAL TO V_T
                # BECAUSE THEY ARE BOTH FROM THE SAME MODEL, WITH NOW
                # EXTERNAL IMPACT ON WHETHER TO UPDATE THE VALUE FUNCTION.
                # THEREFORE, WE NEED TO ENFORCE THAT WHEN WE SEE AN END
                # STATE, WE DO NOT USE THE VALUE FUNCTION, AND PROVIDE
                # THE RELEVANT VALUE INTO THE TENSOR.
                #print(weights.grad)
                self.eligibility_traces[i] = ((gamma * self.lamda * self.eligibility_traces[i])
                                              + weights.grad)

                # Parameter Update:
                # theta <- theta + (alpha * delta * gradient of Q-function)
                new_weights = (weights +
                               (alpha * delta * self.eligibility_traces[i]))
                weights = deepcopy(new_weights)


# END FILE ----------------------------------------------------------- #