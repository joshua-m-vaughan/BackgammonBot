# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan.
# Date:    30/07/2024
# Purpose: Implements an agent that infers from a QFunction for
#          evaluation.

# IMPORTS ------------------------------------------------------------ #

import random
from Agents.rl.tdgammon.TDGammonNN import TDGammonNNQFunction
from Agents.rl.tdgammon.TDGammonMDP import TDGammonMDP
from BackgammonGame.backgammon_model import BackgammonState, BackgammonRules
from ExtendedFormGame.template import Agent


# CONSTANTS ---------------------------------------------------------- #

BUFFER_TIME:float = float(0.25)
FIRST_TURN_TIME:float = float(15.0)
SUBSEQUENT_TURN_TIME:float = float(1.0)

# CLASS DEF ---------------------------------------------------------- #  

class myAgent(Agent):
    def __init__(self,_id: int) -> None:
        super().__init__(_id)
    
        # Define data structures to support off-policy TD learning.
        self.qfunction:TDGammonNNQFunction = None
        self.game_rules:BackgammonRules = BackgammonRules()
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
        # Turn on eval mode.
        self.qfunction.nn.eval()

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

        return random.choice(max_actions)  

# END ---------------------------------------------------------------- #