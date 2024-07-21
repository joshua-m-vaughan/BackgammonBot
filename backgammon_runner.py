# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan
# Date:    13/07/2024
# Purpose: Running script to manage training, evaluating, and testing
#          pipelines for backgammon simulation.

# IMPORTS ------------------------------------------------------------ #

import argparse
import sys
import traceback
from importlib import import_module
from ExtendedFormGame.template import Agent
from backgammon_model import BackgammonRules
from ExtendedFormGame.game import Game
from Agents.generic.random_agent import myAgent as RandomAgent
from datetime import datetime, timedelta


# CONSTANTS ---------------------------------------------------------- #

SEED:int = 42 # The meaning of life!
MAX_EPISODES:int = 1000 # Number of training episodes.
MAX_DURATION:int = 1 # Duration of training in hours.
AGENTS_PATH:str = "Agents."
RESULTS_PATH:str = None

# FUNC DEF ----------------------------------------------------------- #

def load_parameters():
    """ load_parameters
    Processes the command used to run game simulations from the command
    line.
    """

    parser = argparse.ArgumentParser(prog="backgammon_runner",
                                     description="Manages the training, evaluation, and testing pipeline for backgammon simulation.")
    
    # Define arguments for each step in the pipeline.
    ## TODO: Implement.

    # Read args from command line
    return parser.parse_args(sys.argv[1:])

def load_agent(agent_names:list,
               module_path:str = AGENTS_PATH) -> tuple[list[Agent], bool]:
    """load_agent
    Returns a list of agents loaded from different paths, extending the
    approach in the extended form game framework from COMP90054
    Assignment 3.   

    Args:
        agent_names (list): Agent names from agent module.
        module_path (str, optional): Path to agent module. Defaults to
        AGENTS_PATH.
    
    Returns:
        tuple[list[Agent], bool]: A list of agents, and a boolean
        indicating if the agents were valid.
    """
    agent_list = [None] * len(agent_names)
    valid_game = True
    for i in range(len(agent_names)):
        tmp_agent = None
        try:
            agent_module = import_module(module_path+agent_names[i])
            tmp_agent = agent_module.myAgent(i)
        except (NameError, ImportError, IOError):
            print('Error: Agent at "' + agent_names[i] + '" could not be loaded!', file=sys.stderr)
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

        print(agent_list)

    return (agent_list, valid_game)

def train(agent_names:list, results_path: str, seed:int = SEED,
          max_episodes:int = MAX_EPISODES,
          max_duration:int = MAX_DURATION) -> bool:
    """train
    A script to control the training of a agent playing backgammon.

    Args:
        agents (list): A list of agents to be used for training.
        results_path (str): String detailing path to store training results.
        max_episodes (int, optional): Number of episodes to train for.
        Defaults to MAX_EPISODES.
        max_duration (int, optional): Duration to train for. Defaults
        to MAX_DURATION.

    Returns:
        bool: Success indicator of training.
    """
    # Initialise training parameters.
    episode:int = 0
    current_time:datetime = datetime.now()
    finish_time:datetime = current_time + timedelta(hours=max_duration)

    while (current_time < finish_time and episode < max_episodes):
        # Create agents.
        assert(len(agent_names) == 2)
        num_agents = 2
        (agent_list, valid_game) = load_agent(agent_names)
        if not valid_game:
            # TECH DEBT: Should I throw some kind of log from here?
            return False
        
        # Reverse the order of players halfway through training.
        if (current_time > (current_time + timedelta(hours=(max_duration*0.5)))
                or episode > ((MAX_EPISODES * 0.5)-1)):
            # NOTE: Since we only have two players, we can just reverse
            # the order of the list.
            agent_list.reverse()

        # Create game.
        bg_rules = BackgammonRules()
        bg_game = Game(bg_rules, agent_list, agent_names, num_agents,
                       seed)
        
        # Run game.
        history = bg_game.run()
        print(history)

        # Update agents based on outcome of the game.
        # TODO: Implement this, including saving of weights.

        # Store the results.
        # TODO: Implement this.

        # Increment training variables.
        episode += 1
        current_time = datetime.now()
    
    # Write training overview details.
    # e.g. elapsed episode time, number of games, agent names.

    return True



# MAIN --------------------------------------------------------------- #

if __name__ == "__main__":
    # Instantiate classes.
    agent_names:list[str] = ["generic.random_agent", "generic.random_agent"]
    train(agent_names, RESULTS_PATH, max_episodes=5)

# END ---------------------------------------------------------------- #