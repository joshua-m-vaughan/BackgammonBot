# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    29/07/2024
# Purpose: Implements an agent for Backgammon using the TD-Gammon 0.0
#          approach outlined by Tesauro's paper.

# Reference List:
#   Tesauro, G. (1995). Temporal difference learning and TD-Gammon.
#   Communications of the ACM, 38(3), 58-68.

# IMPORTS ------------------------------------------------------------ #

from Agents.rl.tdgammon.TDGammonMDP import TDGammonMDP
from Agents.rl.tdgammon.TDGammonNN import TDGammonNNQFunction 
from BackgammonGame.backgammon_model import BackgammonRules, BackgammonState
from pathlib import PureWindowsPath
from ExtendedFormGame import utils
import random

from ExtendedFormGame.template import Agent

# CONSTANTS ---------------------------------------------------------- #

TD_ALPHA:float = 0.7 # As defined in Tesauro paper.
NUM_TDGAMMON1_HIDDEN:int = 40 # As defined, by Tesauro's paper.

# CLASS DEF ---------------------------------------------------------- #  

class myAgent(Agent):

    policy_path:PureWindowsPath = PureWindowsPath(r"Agents/rl/tdgammon/trained_models/")
    policy_filetype:str = ".pt"

    def __init__(self, _id: int) -> None:
        super().__init__(_id)
        self.game_rules:BackgammonRules = BackgammonRules()
    
        # Define data structures to support off-policy TD learning.
        self.qfunction:TDGammonNNQFunction = TDGammonNNQFunction(NUM_TDGAMMON1_HIDDEN, TD_ALPHA)
        self.mdp:TDGammonMDP = TDGammonMDP(self.qfunction, self.game_rules)
        self.turn:int = 0

    def select_action(self, game_state:BackgammonState,
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

        if self.turn == 0:
            # First action: randomly select an action.
            action:tuple = random.choice(actions)
        else:
            # Subsequent action: Bandit select next action.
            action:tuple = self.qfunction.get_arg_max(game_state, actions)

            # Observe reward
            next_game_state:BackgammonState = self.mdp.get_next_state(game_state, action, self.id)
            next_actions:list[tuple] = self.mdp.get_actions(next_game_state, next_game_state.current_agent_id)
            reward:list[float] = self.mdp.get_reward(game_state,
                                                     next_game_state,
                                                     action,
                                                     self.id)
            
            # Update Q-function using off-policy approach.
            self.qfunction.update(game_state, next_game_state, next_actions,
                                  reward, self.mdp.gamma, self.id)

        # Update turn.
        self.turn += 1

        return action  
    
    # I/O Helpers ---------------------------------------------------- #
    def update_endgame_weights(self, history:dict) -> None:
        """update_endstate_weights
        Updates the weights using the history printout for the match to
        accurately capture rewards at endgame state.

        Args:
            history (dict): Dictionary storing winning results and the
            history for the game.
        """
        utils.raiseNotDefined
        return 0
    
    def save_weights(self, filepath:str) -> None:
        """save_weights
        Save training weights for learning-based agents.
        """
        file_str:PureWindowsPath = PureWindowsPath(myAgent.policy_path,
                                                   filepath+myAgent.policy_filetype)
        self.qfunction.save_policy(file_str)

# END ---------------------------------------------------------------- #