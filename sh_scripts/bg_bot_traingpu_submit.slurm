#!/bin/bash
#SBATCH --job-name=bg_bot_gputrain_$1                                   # Job name
#SBATCH --mail-user=jmv132@stanford.edu                                 # Email address
#SBATCH --mail-type=NONE                                                # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --partition=normal                                              # Node partition
#SBATCH --nodes=1                                                       # Number of nodes requested
#SBATCH --ntasks=1                                                      # Number of processes
#SBATCH --time=0-04:00:00                                               # Time limit request
#SBATCH -p=gpu-pascal

# Execute training script in boardgame container.
apptainer run ./python311_boardgame ./backgammon_runner.py --train --name tdgammon0_0_selfplay --episodes $1 --duration 4 -a rl.tdgammon.TDGammon0_0,rl.tdgammon.TDGammon0_0 --agent_names tdg00_$1_1,tdg00_$1_2 -r $2