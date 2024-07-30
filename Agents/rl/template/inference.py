# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan.
# Date:    30/07/2024
# Purpose: Implements an agent that infers from a QFunction for
#          evaluation.

# IMPORTS ------------------------------------------------------------ #

from Agents.rl.template.qfunction import QFunction
from ExtendedFormGame.template import Agent, GameState

# CONSTANTS ---------------------------------------------------------- #

BUFFER_TIME:float = float(0.25)
FIRST_TURN_TIME:float = float(15.0)
SUBSEQUENT_TURN_TIME:float = float(1.0)

# CLASS DEF ---------------------------------------------------------- #  

class myAgent(Agent):
    def __init__(self,_id: int) -> None:
        super().__init__(_id)
    
        # Define data structures to support off-policy TD learning.
        self.qfunction:QFunction = None
        self.turn:int = 0

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
        return self.qfunction.get_arg_max(game_state, actions)     

# END ---------------------------------------------------------------- #