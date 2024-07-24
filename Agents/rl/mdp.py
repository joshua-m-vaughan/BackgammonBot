# INFORMATION ------------------------------------------------------------------------------------------------------- #

# Author:  Josh Vaughan
# Date:    24/07/2024
# Purpose: Implements MDP representation of a board game.

# IMPORTS ------------------------------------------------------------------------------------------------------------#

from ExtendedFormGame.template import GameRules, GameState
from ExtendedFormGame import utils
from Agents.rl.qfunction import QFunction

# CONSTANTS ----------------------------------------------------------------------------------------------------------#

DISCOUNT_FACTOR:float = float(0.1)

# CLASS DEF ----------------------------------------------------------------------------------------------------------#       

class MDP():

    def __init__(self, qfunction:QFunction,
                 game_rules:GameRules,
                 gamma:float = DISCOUNT_FACTOR) -> None:
        
        self.gamma:float = gamma
        self.qfunction:QFunction = qfunction
        self.game_rules:GameRules = game_rules

    def get_actions(self, game_state:GameState, agent_id:int) -> list[tuple]:
        """ get_actions
        Return a list of actions using the game rules.
        
        Args:
            game_state (GameState): State s
            agent_id (int): Integer representing agent id.

        Returns:
            list[tuple]: A list of tuples representing the actions.
        """
        return self.game_rules.get_legal_actions(game_state, agent_id)

    def get_next_state(self, game_state:GameState, action:tuple,
                       agent_id:int) -> GameState:
        """ get_next_state
        Return the next game_state using the game rules.

        Args:
            game_state (GameState): State s
            action (tuple): Action a
            agent_id (int): Integer representing agent id.

        Returns:
            GameState: State s' that is generated from applying action
            a in state s.
        """
        return self.game_rules.generate_successor(game_state, action, agent_id)

    def get_reward(self, game_state:GameState, game_state_p:GameState,
                  action:tuple, agent_id:int) -> list[float]:
        """ get_reward
        Return reward for transition from s to s' with action a.

        Args:
            game_state (GameState): State s
            game_state_p (GameState): State s'
            action (tuple): Action a
            agent_id (int): Integer representing agent id.

        Returns:
            list[float]: Reward for each agent id, when moving from
            state s to state s'.
        """
        utils.raiseNotDefined()
        return 0
    
    def is_terminal_state(self, game_state:GameState) -> bool:
        """ is_terminal_state
        Return boolean indicating whether terminal game_state reached.

        Args:
            game_state (GameState): State s

        Returns:
            Boolean: Terminal game_state of game_state s.
        """
        return self.game_rules.game_ends(game_state)


# END FILE -----------------------------------------------------------------------------------------------------------#
