from datetime import timedelta
from pathlib import Path
import json
import csv
from backgammon_model import BLACK_ID, WHITE_ID, BackgammonRules, generate_td_gammon_vector

JSON_INDENT:int = 4 # One tab

def initialise_results(agent_path:list[str], agent_names:list[str],
                       model_path:list[str], seed:int) -> dict:
    # Initialise matches dictionary.
    matches:dict = dict()
    matches.update({"seed":seed})
    matches.update({"games":[]})
    matches.update({"num_games": 0})
    matches.update({"wins":[0]*len(agent_path)})
    matches.update({"ties":[0]*len(agent_path)})
    matches.update({"losses":[0]*len(agent_path)})
    matches.update({"teams":[]})

    # Insert agents into log.
    for i in range(len(agent_path)):
        team_info:dict = dict()
        team_info["agent"] = agent_path[i]
        team_info["team_name"] = agent_names[i]
        matches["teams"].append(team_info)
    
    return matches

def checkpoint_results(matches:dict, history:dict, results_path:str,
                       file_time:str, name:str, seed:float,
                       episode:int, elapsed:timedelta) -> dict:
    # Store the history trace.
    # NOTE: Evaluate whether I could setup a MongoDB with PyMongo.
    file_str = results_path + file_time + "_" + name + "_" + str(episode) + ".json"
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
    game.update({"filename":file_time + "_" + name + "_" + str(episode)})
    game.update({"random_seed":seed})
    game.update({"scores":history["scores"]})
    game.update({"training_time":str(elapsed)})
    matches["games"].append(game)
    matches.update({"num_games": episode})

    # Update wins and losses.
    for i in range(len(matches["teams"])):
            if (history["scores"][i] == 1):
                matches["wins"][i] += 1
            else:
                matches["losses"][i] += 1

    return matches

def save_results(matches:dict, results_path:str,
                 file_time:str, name:str):
    matches.update({"win_percentage": [w/matches["num_games"] for w in matches["wins"]]})
    matches.update({"succ":True})

    file_str = results_path + file_time + "_" + name + "_matches.json"
    match_filename = Path(file_str)
    with open(match_filename, "w") as file:
        serialised = {str(key): value for key, value in matches.items()}
        json.dump(serialised, file, indent=JSON_INDENT)

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

    black_agent:str = match["teams"][BLACK_ID]["agent"]
    white_agent:str = match["teams"][WHITE_ID]["agent"]
    header = ["black_agent_name", "white_agent_name", "board_vector",
              "match_winner"]

    # Open file.
    csv_file = open(out_filename, "w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)

    for m_game in match["games"]:
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
                
                break
        # Store board position.
        csv_writer.writerow([black_agent, white_agent, selected_board_vector, won_game])

    # All positions have been extracted.
    csv_file.close()
    assert(csv_file.closed)

    return None

def time_print(s:str):
    print("[{}] {}".format(datetime.now().strftime("%H:%M:%S"), s))
