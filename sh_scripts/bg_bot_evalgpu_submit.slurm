#!/bin/bash
#SBATCH --job-name=bg_bot_evalgpu_$1                                    # Job name
#SBATCH --mail-user=jmv132@stanford.edu                                 # Email address
#SBATCH --mail-type=NONE                                                # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --partition=normal                                              # Node partition
#SBATCH --nodes=1                                                       # Number of nodes requested
#SBATCH --ntasks=1                                                      # Number of processes
#SBATCH --time=0-04:00:00                                               # Time limit request
#SBATCH --output=~./BackgammonBot/sh_scripts/sbatch_logs/slurm-%a.out   # STDOUT
#SBATCH --partition=gpu_pascal                                          # GPU node to run on

# Execute training script in boardgame container.
apptainer run ./python311_boardgame ./backgammon_runner.py --eval --name tdgammon0_0_eval --episodes $1 --duration 4 --set_seed $2 -a rl.template.inference,rl.template.inference --agent_names tdg00_$1_1,tdg00__$1_2 --models $3,$4 -r $5