import itertools
from Agents.rl.tdgammon.TDGammon0_0 import myAgent
import torch
from pathlib import Path

TD1000:str = "20240801-0052_tdgammon0_0_selfplay_cpu1000.pt"
TD5000:str = "20240801-1949_tdgammon0_0_selfplay_gpu5000.pt"
TD10000:str = "20240802-2027_tdgammon0_0_selfplay_cpu10000.pt"
TD15000:str = "20240801-0750_tdgammon0_0_selfplay_cpu15000.pt"

REV_5:str = "20240805-1456_debug.pt"
REV_20:str = "20240805-1457_debug.pt"

PATHS = [REV_5, REV_20]

if __name__ == "__main__":

    agents = []
    for i in range(len(PATHS)):
        agents.append(myAgent(i))
        agents[i].qfunction.load_policy(Path(myAgent.policy_path, PATHS[i]))

    for (agent_i, agent_j) in itertools.combinations(agents, 2):
            equality = True
            if (id(agent_i) != id(agent_j)):
                assert (len(agent_i.qfunction.nn.eligibility_traces) == 
                        len(agent_j.qfunction.nn.eligibility_traces))
                
                for i in range(len(agent_i.qfunction.nn.eligibility_traces)):
                    if (not torch.equal(agent_i.qfunction.nn.eligibility_traces[i], agent_j.qfunction.nn.eligibility_traces[i])):
                        equality = False
                
                if equality:
                    print("Agent" + str(agent_i.id) + " Agent" + str(agent_j.id) + " etraces are equal.")
                else:
                    print("Agent" + str(agent_i.id) + " Agent" + str(agent_j.id) + " etraces are not equal.")
                

                equality = True
                agent_i_param = list(agent_i.qfunction.nn.parameters())
                agent_j_param = list(agent_j.qfunction.nn.parameters())
                assert (len(agent_i_param) == len(agent_j_param))
                for i in range(len(agent_i_param)):
                    ai_weight = agent_i_param[i]
                    aj_weight = agent_j_param[i]
                    if (not torch.equal(ai_weight, aj_weight)):
                        equality = False

                if equality:
                    print("Agent" + str(agent_i.id) + " Agent" + str(agent_j.id) + " weights are equal.")
                else:
                    print("Agent" + str(agent_i.id) + " Agent" + str(agent_j.id) + " weights are not equal.")
                
                print()