#!/bin/bash
#SBATCH --job-name=bg_bot_evalcpu_$1                                    # Job name
#SBATCH --mail-user=jmv132@stanford.edu                                 # Email address
#SBATCH --mail-type=NONE                                                # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --partition=normal                                              # Node partition
#SBATCH --nodes=1                                                       # Number of nodes requested
#SBATCH --ntasks=1                                                      # Number of processes
#SBATCH --time=1-00:00:00                                               # Time limit request

# Execute training script in boardgame container.
apptainer run ./python311_boardgame ./backgammon_runner.py --eval --name tdg00_eval --episodes $1 --duration 24 --set_seed $2 -a rl.tdgammon.inference,rl.tdgammon.inference --agent_names $3,$4 --models $3,$4 -r $5