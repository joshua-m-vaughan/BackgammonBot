#!/bin/bash
#SBATCH --job-name="bg_bot_train"           # Job name
#SBATCH --mail-user=jmv132@stanford.edu     # Email address
#SBATCH --mail-type=NONE                    # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --partition=normal                  # Node partition
#SBATCH --nodes=1                           # Number of nodes requested
#SBATCH --ntasks=1                          # Number of processes
#SBATCH --time=1-00:00:00                     # Time limit request

# Execute training script in boardgame container.
apptainer run ./python311_boardgame ./backgammon_runner.py --eval --name tdgammon0_0_eval_test --episodes 5 -a rl.template.inference,rl.template.inference --agent_names tdg00_v1,tdg00_v2 --models Agents/rl/tdgammon/trained_models/20240801-0018_tdgammon0_0_selfplay_v1.pt,Agents/rl/tdgammon/trained_models/20240801-0018_tdgammon0_0_selfplay_v1.pt -r "results/eval"
