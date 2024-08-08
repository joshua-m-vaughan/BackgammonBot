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

from re import A
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

        # Select the highest estimated outcome state value.
        max_value:float = float("-inf")
        max_actions:list[tuple] = []

        for a in actions:
            tmp_game_state_p:BackgammonState = self.mdp.get_next_state(game_state, a, self.id)
            tmp_value:float = self.qfunction.get_q_value(tmp_game_state_p, None)[self.id]
            if tmp_value > max_value:
                max_value = tmp_value
                max_actions = [a]
            elif tmp_value == max_value:
                max_actions.append(a)

        action:tuple = random.choice(max_actions)

        # Update Q-Function.
        next_game_state:BackgammonState = self.mdp.get_next_state(game_state, action, self.id)
        reward:float = self.mdp.get_reward(game_state, next_game_state, action, self.id)
        self.qfunction.update(game_state, next_game_state, None,
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