# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan
# Date:    13/07/2024
# Purpose: Running script to manage training, evaluating, and testing
#          pipelines for backgammon simulation.

# IMPORTS ------------------------------------------------------------ #

import argparse
import sys
from ExtendedFormGame.template import Agent
from backgammon_model import BackgammonRules
from ExtendedFormGame.game import Game
from Agents.generic.random_agent import RandomAgent
from datetime import datetime, timedelta

# CONSTANTS ---------------------------------------------------------- #

SEED:int = 42 # The meaning of life!
MAX_EPISODES:int = 1000 # Number of training episodes.
MAX_DURATION:int = 1 # Duration of training in hours.

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
        agent_list = []
        # TODO: Reverse halfway through training.

        # Create game.
        bg_rules = BackgammonRules()
        bg_game = Game(bg_rules, agent_list, agent_names, num_agents,
                       seed)
        
        # Run game.
        history = bg_game.run()

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
    bg_rules:BackgammonRules = BackgammonRules()
    bg_random_one:Agent = RandomAgent(0)
    bg_random_two:Agent = RandomAgent(1)
    agent_list: list[tuple] = [bg_random_one, bg_random_two]
    agent_names:list[str] = ["rand_one", "rand_two"]

    bg = Game(bg_rules, agent_list, agent_names, 2, SEED)
    history = bg.run()
    print("\n"*3)
    print("History: ")
    print(history)

# END ---------------------------------------------------------------- #