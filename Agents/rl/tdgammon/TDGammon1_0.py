# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    29/07/2024
# Purpose: Implements an agent for Backgammon using the TD-Gammon 1.0
#          approach outlined by Tesauro's paper.

# Reference List:
#   Tesauro, G. (1995). Temporal difference learning and TD-Gammon.
#   Communications of the ACM, 38(3), 58-68.

# IMPORTS ------------------------------------------------------------ #

from Agents.rl.td.td_offpolicy import OffPolicyTDAgent
from Agents.rl.tdgammon.TDGammonMDP import TDGammonMDP
from Agents.rl.template.bandit import SoftMaxBandit
from Agents.rl.tdgammon.TDGammonNN import TDGammonNNQFunction 
from backgammon_model import BackgammonRules

# CONSTANTS ---------------------------------------------------------- #

TD_ALPHA:float = 0.7 # As defined in Tesauro paper.
NUM_TDGAMMON1_HIDDEN:int = 40 # As defined, by Tesauro's paper.

# CLASS DEF ---------------------------------------------------------- #  

class myAgent(OffPolicyTDAgent):

    def __init__(self, _id: int) -> None:
        tmp_q = TDGammonNNQFunction(NUM_TDGAMMON1_HIDDEN, TD_ALPHA)
        tmp_gr = BackgammonRules()
        super().__init__(_id,
                         tmp_q,
                         tmp_gr,
                         TDGammonMDP(tmp_q, tmp_gr),
                         SoftMaxBandit(tmp_q))


# END ---------------------------------------------------------------- #