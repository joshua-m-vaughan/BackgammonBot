# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan
# Date:    29/07/2024
# Purpose: Implements MDP representation of a Backgammon Boardgame using
#          the TD-Gammon 1.0 approach outlined by Tesauro's paper.

# Reference List:
#   Tesauro, G. (1995). Temporal difference learning and TD-Gammon.
#   Communications of the ACM, 38(3), 58-68.

# IMPORTS ------------------------------------------------------------ #

from Agents.rl.template.mdp import MDP
from Agents.rl.template.qfunction import QFunction
from backgammon_model import BackgammonRules, BackgammonState

# CONSTANTS ---------------------------------------------------------- #

# CLASS DEF ---------------------------------------------------------- #      

class TDGammonMDP(MDP):

    def __init__(self, qfunction:QFunction,
                 game_rules:BackgammonRules,
                 gamma = None) -> None:
        
        if gamma is None:
            super().__init__(qfunction, game_rules)
        else:
            super().__init__(qfunction, game_rules, float(gamma))

    def get_reward(self, game_state:BackgammonState,
                   game_state_p:BackgammonState,
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
        reward:list[float] = []
        for i in range(game_state_p.num_agents):
            tmp_result:float = float(self.game_rules.calculate_endgame_score(game_state_p, i))
            reward.append(tmp_result)
        
        return reward

# END FILE ----------------------------------------------------------- #