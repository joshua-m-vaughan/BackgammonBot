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
from pathlib import Path
import json
from ExtendedFormGame.template import Agent
from backgammon_model import BLACK_ID, WHITE_ID, BackgammonRules, generate_td_gammon_vector
from ExtendedFormGame.Game import Game
from Agents.generic.random import myAgent as RandomAgent
from datetime import datetime, timedelta
import random
import csv

# CONSTANTS ---------------------------------------------------------- #

SEED:int = 42 # The meaning of life!
MAX_EPISODES:int = 1000 # Number of training episodes.
MAX_DURATION:int = 1 # Duration of training in hours.
AGENTS_PATH:str = "Agents."
RESULTS_PATH:str = "Results\\"
JSON_INDENT:int = 4 # One tab

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
    file_time:datetime = current_time.strftime("%Y%m%d-%H%M")
    wins:list[int] = [0] * len(agent_names)
    ties:list[int] = [0] * len(agent_names)
    losses:list[int] = [0] * len(agent_names)

    # Initialise matches dictionary.
    matches:dict = dict()
    matches.update({"games":[]})
    matches.update({"teams":[]})
    matches.update({"num_games": episode})

    # Insert agents into log.
    for i in range(len(agent_names)):
        team_info:dict = dict()
        team_info["agent"] = agent_names[i]
        team_info["team_name"] = "TODO"
        matches["teams"].append(team_info)

    while (current_time < finish_time and episode < max_episodes):
        # Create agents.
        assert(len(agent_names) == 2)
        num_agents = 2
        (agent_list, valid_game) = load_agent(agent_names)
        if not valid_game:
            # TECH DEBT: Should I throw some kind of log from here?
            return False
        
        # TODO: FIX GAME LOGGING TO HANDLE THE REVERSION.
        # Reverse the order of players halfway through training.
        #if (current_time > (current_time + timedelta(hours=(max_duration*0.5)))
        #        or episode > ((MAX_EPISODES * 0.5)-1)):
        #    # NOTE: Since we only have two players, we can just reverse
        #    # the order of the list.
        #    agent_list.reverse()


        # Create game.
        bg_rules = BackgammonRules()
        bg_game = Game(bg_rules, agent_list, agent_names, num_agents,
                       seed)
        
        # Run game.
        history = bg_game.run()
        print(history)

        # Update agents weights based on outcome of the game.
        # TODO: Implement this, including saving of weights.

        # Store the results.
        # NOTE: Evaluate whether I could setup a MongoDB with PyMongo.
        file_str = results_path + file_time + "_" + str(episode) + ".json"
        filename = Path(file_str)
        with open(filename, "w") as file:
            serialised = {str(key): value for key, value in history.items()}
            json.dump(serialised, file, indent=JSON_INDENT)
        
        # Store training-level results.
        game:dict = dict()
        game.update({"valid_game":True})
        for score in history["scores"]:
            if score < 0:
                game.update({"valid_game":False})
                break
        game.update({"filename":file_time + "_" + str(episode)})
        game.update({"random_seed":seed})
        game.update({"scores":history["scores"]})
        matches["games"].append(game)
        matches.update({"num_games": episode})

        for i in range(len(agent_names)):
            if (history["scores"][i] == 1):
                wins[i] += 1
            else:
                losses[i] += 1

        # Increment training variables.
        episode += 1
        current_time = datetime.now()
    
    # Write training overview details.
    # e.g. elapsed episode time, number of games, agent names.
    matches.update({"wins":wins})
    matches.update({"ties":ties})
    matches.update({"losses":losses})
    matches.update({"win_percentage":[w/episode for w in wins]})
    matches.update({"succ":True})

    file_str = results_path + file_time + "_matches.json"
    match_filename = Path(file_str)
    with open(match_filename, "w") as file:
        serialised = {str(key): value for key, value in matches.items()}
        json.dump(serialised, file, indent=JSON_INDENT)

    return True


def extract_board_positions(match_filename:str, out_filename:str) -> None:
    """extract_board_positions
    Returns a list of tuples that stores the black agent name, white
    agent name, the randomly selected board position, and the winner of
    the game.

    Args:
        filename (str): String detailing the file_name of the matches
        training epoch summary.

    Returns:
        list[tuple]: _description_
    """

    with open(match_filename, "r") as m_file:
        match:dict = json.load(m_file)

    print(match)
    black_agent:str = match["teams"][BLACK_ID]["agent"]
    white_agent:str = match["teams"][WHITE_ID]["agent"]
    header = ["black_agent_name", "white_agent_name", "board_vector",
              "match_winner"]

    # Open file.
    csv_file = open(out_filename, "w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)

    for m_game in match["games"]:
        print(m_game)

        with open("Results\\"+m_game["filename"]+".json", "r") as g_file:
            game:dict = json.load(g_file)

        # Select a random board position.
        selected_pos_num = random.randrange(0, len(game["actions"]))
        
        # Simulate game to that board position.
        bg_rules = BackgammonRules()
        for turn in game["actions"]:
            # Simulate the action.
            assert(type(turn["action"]) is list)
            for move in turn["action"]:
                assert(type(move) is list)
            bg_rules.update(turn["action"])

            # Determine if this is the relevant board position.
            if turn["turn"] == selected_pos_num:
                # Generate vector representation.
                selected_board_vector = generate_td_gammon_vector(bg_rules.current_game_state)
                # Determine who won.
                if (bg_rules.current_agent_id == BLACK_ID
                    and game["scores"][BLACK_ID]):
                    won_game:int = 1
                elif (bg_rules.current_agent_id == WHITE_ID
                    and game["scores"][WHITE_ID]):
                    won_game:int = 1
                else:
                    won_game:int = -1
                
                print(bg_rules.current_agent_id)
                print(game["scores"])
                break
        # Store board position.
        csv_writer.writerow([black_agent, white_agent, selected_board_vector, won_game])

    # All positions have been extracted.
    csv_file.close()
    assert(csv_file.closed)

    return None

# MAIN --------------------------------------------------------------- #

if __name__ == "__main__":
    # Instantiate classes.
    random.seed(SEED)
    #agent_names:list[str] = ["generic.random", "heuristic.running"]
    #train(agent_names, RESULTS_PATH, max_episodes=5)

    extract_board_positions("Results\\20240726-1055_matches.json",
                            "Results\\20240726-1055_board_value.csv")

# END ---------------------------------------------------------------- #