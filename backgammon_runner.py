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

# CONSTANTS ---------------------------------------------------------- #

SEED:int = 42 # The meaning of life!

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