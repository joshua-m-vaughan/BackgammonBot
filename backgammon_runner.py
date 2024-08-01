# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan
# Date:    XX/07/2024
# Purpose: Running script to manage training, evaluating, and testing
#          pipelines for backgammon simulation.

# IMPORTS ------------------------------------------------------------ #

import argparse
from pathlib import PurePosixPath, PureWindowsPath
import sys
import traceback
from importlib import import_module
from Agents.rl.td.td_offpolicy import OffPolicyTDAgent
from Agents.rl.tdgammon.TDGammonNN import TDGammonNNQFunction
from Agents.rl.template.inference import myAgent as InferenceAgent
from ExtendedFormGame.template import Agent
from backgammon_model import BLACK_ID, WHITE_ID, BackgammonRules
from ExtendedFormGame.Game import Game
from Agents.generic.random import myAgent as RandomAgent
from datetime import datetime, timedelta
import random
import re

from supportils import initialise_results, checkpoint_results, save_results, time_print

# CONSTANTS ---------------------------------------------------------- #

SEED:int = 42 # The meaning of life!
BASE_EPISODES:int = 5 # Number of training episodes.
BASE_DURATION:int = 1 # Duration of training in hours.
AGENTS_MODULE_PATH:str = "Agents."
RESULTS_PATH:PureWindowsPath = PureWindowsPath("results", "train")
JSON_INDENT:int = 4 # One tab

# FUNC DEF ----------------------------------------------------------- #

def load_parameters():
    """ load_parameters
    Processes the command used to run game simulations from the command
    line.
    """

    parser = argparse.ArgumentParser(prog="backgammon_runner",
                                     description="Manages the training, evaluation, and testing pipeline for backgammon simulation.")
    
    # Training/Evaluation.
    parser.add_argument("-t", "--train", action='store_true', help="Boolean indicator of whether performing training. (default: False)", default=False, dest="train")
    parser.add_argument("-e", "--eval", action='store_true', help="Boolean indicator of whether performing evaluation. (default: False)", default=False, dest="eval")
    parser.add_argument("-n", "--name", help="A string used to provide additional identification to runtime logs.", default="", dest="name")
    parser.add_argument("--episodes", type=int, help="Number of episodes in training or evaluation for simulation. (default=5)", default=BASE_EPISODES, dest="episodes")
    parser.add_argument("--duration", type=int, help="Duration (in hours) of training or evaluation for simulation. (default=1)", default=BASE_DURATION, dest="duration")

    # Agents.
    parser.add_argument('-a','--agents', help='A list of the agents, etc, agents.myteam.player', default="generic.random,generic.random", dest="agents")
    parser.add_argument('--agent_names', help='A list of agent names', default="random0,random1", dest="agent_names") 
    parser.add_argument("-m", "--models", help="A list of paths to agent models.", dest="models")

    # Game settings.
    parser.add_argument('-w', '--warningTimeLimit', type=float,help='Time limit for a warning of one move in seconds (default: 1)', default=1.0, dest="wtl")
    parser.add_argument('--num_warnings', type=int,help='Num of warnings a team can get before fail (default: 3)', default=3, dest="num_warnings")
    parser.add_argument('--set_seed', type=int,help='Set the random seed, otherwise it will be completely random (default: 42)', default=SEED, dest="set_seed")
    parser.add_argument("-r", "--results", help="Path to store results for the runtime. (Default: 'Results')", default=RESULTS_PATH, dest="results")
    # Read args from command line
    return parser.parse_args(sys.argv[1:])

def load_agent(agent_path:list,
               module_path:str = AGENTS_MODULE_PATH) -> tuple[list[Agent], bool]:
    """load_agent
    Returns a list of agents loaded from different paths, extending the
    approach in the extended form game framework from COMP90054
    Assignment 3.   

    Args:
        agent_path (list): Agent names from agent module.
        module_path (str, optional): Path to agent module. Defaults to
        AGENTS_MODULE_PATH.
    
    Returns:
        tuple[list[Agent], bool]: A list of agents, and a boolean
        indicating if the agents were valid.
    """
    agent_list = [None] * len(agent_path)
    valid_game = True
    for i in range(len(agent_path)):
        tmp_agent = None
        try:
            agent_module = import_module(module_path+agent_path[i])
            tmp_agent = agent_module.myAgent(i)
        except (NameError, ImportError, IOError):
            print('Error: Agent at "' + agent_path[i] + '" could not be loaded!', file=sys.stderr)
            traceback.print_exc()
            pass
        finally:
            pass

        # Use a random agent, if agent was unable to be loaded.
        if tmp_agent is not None:
            agent_list[i] = tmp_agent
            # TECH DEBT: Should I have some sort of value to store the success of the agents loaded?
        else:
            valid_game = False
            agent_list[i] = RandomAgent(i)
            # TECH DEBT: Should I have some sort of value to store the success of the agents loaded?

    return (agent_list, valid_game)

def train(agent_path:list[str], agent_names:list[str],
          results_path: str, training_name:str, seed:int = SEED,
          max_episodes:int = BASE_EPISODES,
          max_duration:int = BASE_DURATION) -> bool:
    """train
    A script to control the training of a agent playing backgammon.

    Args:
        agent_path(list[str]): A list of agent paths for training.
        agents (list[str]): A list of agents names in the training.
        results_path (str): String detailing path to store training results.
        training_name(str): String providing context to training example.
        seed(int): Integer for random seed.
        max_episodes (int, optional): Number of episodes to train for.
        Defaults to BASE_EPISODES.
        max_duration (int, optional): Duration to train for. Defaults
        to BASE_DURATION.

    Returns:
        bool: Success indicator of training.
    """
    # Initialise training parameters.
    episode:int = 0
    current_time:datetime = datetime.now()
    finish_time:datetime = current_time + timedelta(hours=max_duration)
    file_time:datetime = current_time.strftime("%Y%m%d-%H%M")
    random.seed(seed)

    # Initialise matches dictionary.
    matches:dict = initialise_results(agent_path, agent_names,
                                      model_path, seed)

    # Create agents.
    time_print("Creating agents...")
    assert(len(agent_path) == 2)
    num_agents = 2
    (agent_list, valid_game) = load_agent(agent_path)
    # Self-play game between TD Agents.
    if (agent_path[BLACK_ID] == agent_path[WHITE_ID]
        and type(agent_path[BLACK_ID]) is OffPolicyTDAgent
        and type(agent_path[WHITE_ID]) is OffPolicyTDAgent):
        # Both agents reference the same Q-Function.
        agent_list[WHITE_ID].qfunction = agent_list[BLACK_ID].qfunction
        assert(id(agent_list[WHITE_ID].qfunction) == id(agent_list[BLACK_ID].qfunction))
    # Invalid agent loading.
    if not valid_game:
        # TECH DEBT: Should I throw some kind of log from here?
        return False

    while (datetime.now() < finish_time and episode < max_episodes):
        time_print(f"Starting episode {episode}...")
        start:datetime = datetime.now()
        
        # TODO: FIX GAME LOGGING TO HANDLE THE REVERSION.
        # Reverse the order of players halfway through training.
        #if (current_time > (current_time + timedelta(hours=(max_duration*0.5)))
        #        or episode > ((BASE_EPISODES * 0.5)-1)):

        # Create game.
        tmp_seed:float = random.random()
        bg_rules = BackgammonRules()
        bg_game = Game(bg_rules, agent_list, agent_path, num_agents,
                       tmp_seed)
        
        # Run game.
        history = bg_game.run()

        # Update agents weights based on outcome of the game.
        # TODO: NOTE: Very unsure about how to implement this.

        elapsed:datetime = datetime.now() - start
        time_print(f"Elapsed episode time {elapsed}")
        time_print("Checkpointing results...\n")

        # Increment training variables.
        episode += 1

        # Checkpoint results
        matches = checkpoint_results(matches, history, results_path,
                                     file_time, training_name, tmp_seed,
                                     episode, elapsed)

        # Checkpoint training weights.
        for agent in agent_list:
            filepath:PureWindowsPath = PureWindowsPath(file_time+"_"+training_name)
            file_str:str = str(PurePosixPath(filepath))
            agent.save_weights(file_str)
    
    time_print("Saving epoch results...")

    # Write training overview details.
    matches = save_results(matches, results_path, file_time,
                           training_name)

    time_print("Training Complete.")
    return True

def eval(agent_path:list[str], agent_names:list[str],
         model_path:list[str], results_path: str,
         eval_name:str, seed:int = SEED,
         max_episodes:int = BASE_EPISODES,
         max_duration:int = BASE_DURATION) -> bool:
    """eval
    A script to control the evaluation of an agent playing backgammon.

    Args:
        agent_path(list[str]): A list of agent paths for training.
        agents (list[str]): A list of agents names in the training.
        model_path(list[str]): A list of model paths for evaluation.
        results_path (str): String detailing path to store evaluation results.
        eval_name(str): String providing context to evaluation example.
        seed(int): Integer for random seed.
        max_episodes (int, optional): Number of episodes to evaluate for.
        Defaults to BASE_EPISODES.
        max_duration (int, optional): Duration to evaluate for. Defaults
        to BASE_DURATION.

    Returns:
        bool: Success indicator of evaluation.
    """
    # Initialise training parameters.
    episode:int = 0
    current_time:datetime = datetime.now()
    finish_time:datetime = current_time + timedelta(hours=max_duration)
    file_time:datetime = current_time.strftime("%Y%m%d-%H%M")
    random.seed(seed)

    # Initialise matches dictionary.
    matches:dict = initialise_results(agent_path, agent_names,
                                      model_path, seed)

    # Create agents.
    time_print("Creating agents...")
    assert(len(agent_path) == 2)
    num_agents = 2
    (agent_list, valid_game) = load_agent(agent_path)
    # Invalid agent loading.
    if not valid_game:
        # TECH DEBT: Should I throw some kind of log from here?
        return False
    
    # Load models for evaluation.
    for i in range(num_agents):
        if type(agent_list[i]) is InferenceAgent:
            # TD Gammon NN Qfunction provided.
            if re.search(r"(Agents\\rl\\tdgammon\\trained_models\\)(.*)", model_path[i]):
                agent_list[i].qfunction = TDGammonNNQFunction()
                agent_list[i].qfunction.load_policy(model_path[i])
            else:
                return False

    while (datetime.now() < finish_time and episode < max_episodes):
        time_print(f"Starting episode {episode}...")
        start:datetime = datetime.now()
        
        # TODO: FIX GAME LOGGING TO HANDLE THE REVERSION.
        # Reverse the order of players halfway through training.
        #if (current_time > (current_time + timedelta(hours=(max_duration*0.5)))
        #        or episode > ((BASE_EPISODES * 0.5)-1)):

        # Create game.
        tmp_seed:float = random.random()
        bg_rules = BackgammonRules()
        bg_game = Game(bg_rules, agent_list, agent_path, num_agents,
                       tmp_seed)
        
        # Run game.
        history = bg_game.run()

        # Store the results.
        elapsed:datetime = datetime.now() - start
        time_print(f"Elapsed episode time {elapsed}")
        time_print("Checkpointing results...\n")

        # Increment training variables.
        episode += 1

        # Checkpoint results
        matches = checkpoint_results(matches, history, results_path,
                                     file_time, eval_name, tmp_seed,
                                     episode, elapsed)
    
    time_print("Saving epoch results...")

    # Write training overview details.
    matches = save_results(matches, results_path, file_time,
                           eval_name)

    time_print("Evaluation Complete.")
    return True

# MAIN --------------------------------------------------------------- #

if __name__ == "__main__":
    options = load_parameters()
    time_print(str(options))
    
    # Fill in instances.
    agent_path:list[str] = str(options.agents).split(",")
    agent_names:list[str] = str(options.agent_names).split(",")
    model_path:list[str] = str(options.models).split(",")
    wtl:float = options.wtl
    num_warnings:int = options.num_warnings
    random.seed(options.set_seed)
    results_path:PureWindowsPath = PureWindowsPath(options.results)

    name:str = options.name
    max_episodes:int = options.episodes
    max_duration:int = options.duration

    # Determine run-time.
    if options.train:
        train(agent_path, agent_names, results_path, name,
              options.set_seed, max_episodes, max_duration)
    elif options.eval:
        eval(agent_path, agent_names, model_path, results_path,
             name, options.set_seed, max_episodes, max_duration)

    exit()

    # Example options:
    # --train --name tdgammon0_0_selfplay --episodes 5 -a rl.tdgammon.TDGammon0_0,rl.tdgammon.TDGammon0_0 --agent_names tdg00_1,tdg00_2
    # --eval --name tdgammon0_0_eval_test --episodes 5 -a rl.template.inference,rl.template.inference --agent_names tdg00_v1,tdg00_v2 --models Agents\rl\tdgammon\trained_models\20240730-1656_tdgammon0_0_selfplay_v1.pt,Agents\rl\tdgammon\trained_models\20240730-1656_tdgammon0_0_selfplay_v1.pt -r "results\\eval"

# END ---------------------------------------------------------------- #