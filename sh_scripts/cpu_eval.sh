#!/bin/bash

numGames=500
seed=344
agent500=Agents/rl/tdgammon/trained_models/20240810-1153_tdg00_sp_cpu500.pt
agent1000=Agents/rl/tdgammon/trained_models/20240810-1113_tdg00_sp_cpu1000.pt
agent2000=Agents/rl/tdgammon/trained_models/20240810-1005_tdg00_sp_cpu2000.pt
evalPath=results/eval/presentation_results

sbatch sh_scripts/bg_bot_evalcpu_submit.slurm $numGames $seed $agent500 $agent500 $evalPath
sbatch sh_scripts/bg_bot_evalcpu_submit.slurm $numGames $seed $agent500 $agent1000 $evalPath
sbatch sh_scripts/bg_bot_evalcpu_submit.slurm $numGames $seed $agent500 $agent2000 $evalPath

sbatch sh_scripts/bg_bot_evalcpu_submit.slurm $numGames $seed $agent1000 $agent500 $evalPath
sbatch sh_scripts/bg_bot_evalcpu_submit.slurm $numGames $seed $agent1000 $agent1000 $evalPath
sbatch sh_scripts/bg_bot_evalcpu_submit.slurm $numGames $seed $agent1000 $agent2000 $evalPath

sbatch sh_scripts/bg_bot_evalcpu_submit.slurm $numGames $seed $agent2000 $agent500 $evalPath
sbatch sh_scripts/bg_bot_evalcpu_submit.slurm $numGames $seed $agent2000 $agent1000 $evalPath
sbatch sh_scripts/bg_bot_evalcpu_submit.slurm $numGames $seed $agent2000 $agent2000 $evalPath