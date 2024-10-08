from pathlib import PurePosixPath
import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime

FOLDER_PATH:str = "results/train/presentation_results"
CPU_PATH:PurePosixPath = PurePosixPath(FOLDER_PATH, "20240810-1153_tdg00_sp_cpu500_matches.json")
GPU_PATH:PurePosixPath = PurePosixPath(FOLDER_PATH, "20240810-1001_tdg00_sp_gpu100_matches.json")

episode_dict = dict()
training_name = ["CPU", "GPU"]
training_duration = []

RESULTS_PATHS = [CPU_PATH, GPU_PATH]
for path in RESULTS_PATHS:

    # Load JSON file
    with open(path, "r") as f:
        data = json.load(f)

    # Generate dataframe.
    cpu_game_df = pd.json_normalize(data["games"])
    cpu_game_df["training_time"] = pd.to_datetime(cpu_game_df["training_time"])
    cpu_game_df["training_time"] = cpu_game_df["training_time"] - datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
    cpu_game_df["training_time"] = cpu_game_df["training_time"].dt.total_seconds()
    print(cpu_game_df.head())

    # Store results in data structure.
    episode_dict[path] = list(cpu_game_df["training_time"])
    training_duration.append(cpu_game_df["training_time"].sum())


# Plot Episode duration chart.
plt.plot(range(1,len(episode_dict[GPU_PATH])+1,1), episode_dict[GPU_PATH], label="GPU")
plt.plot(range(1,len(episode_dict[CPU_PATH])+1,1), episode_dict[CPU_PATH], label="CPU")
plt.legend()
plt.xlabel("Episode number")
plt.ylabel("Episode duration (s)")
plt.savefig("res/episode-duration.png", transparent=True)
plt.show()

# Plot Episode duration chart.
plt.bar(training_name, training_duration, width=0.45)
plt.xlabel("Hardware Type")
plt.ylabel("Episode duration (s)")
plt.savefig("res/training-duration.png", transparent=True)
plt.show()