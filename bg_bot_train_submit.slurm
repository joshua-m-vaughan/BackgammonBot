#!/bin/bash
#SBATCH --job-name="bg_bot_train"           # Job name
#SBATCH --mail-user=jmv132@stanford.edu     # Email address    
#SBATCH --mail-type=END                     # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --partition=normal                  # Node partition
#SBATCH --nodes=1                           # Number of nodes requested
#SBATCH --ntasks=1                          # Number of processes
#SBATCH --time=03:00:00                     # Time limit request

# Execute training script in boardgame container.
python311_boardgame ./backgammon_runner.py --train --name tdgammon0_0_selfplay --episodes 5 --duration 3 -a rl.tdgammon.TDGammon0_0,rl.tdgammon.TDGammon0_0 --agent_names tdg00_1,tdg00_2