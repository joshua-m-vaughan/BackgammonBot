#!/bin/bash

numGames = 5000
seed = 344
agent1000 = Agents/rl/tdgammon/trained_models/20240801-0052_tdgammon0_0_selfplay_cpu1000.pt
agent5000 = Agents/rl/tdgammon/trained_models/20240801-1949_tdgammon0_0_selfplay_gpu5000.pt
agent15000 = Agents/rl/tdgammon/trained_models/20240801-0750_tdgammon0_0_selfplay_cpu15000.pt
evalPath = results/eval

sbatch sh_scripts/bg_bot_evalgpu_submit.slurm $numGames $agent1000 $agent1000 $evalPath/20240802_1000v1000
sbatch sh_scripts/bg_bot_evalgpu_submit.slurm $numGames $agent1000 $agent5000 $evalPath/20240802_1000v5000
sbatch sh_scripts/bg_bot_evalgpu_submit.slurm $numGames $agent1000 $agent15000 $evalPath/20240802_1000v15000

sbatch sh_scripts/bg_bot_evalgpu_submit.slurm $numGames $agent5000 $agent1000 $evalPath/20240802_5000v1000
sbatch sh_scripts/bg_bot_evalgpu_submit.slurm $numGames $agent5000 $agent5000 $evalPath/20240802_5000v5000
sbatch sh_scripts/bg_bot_evalgpu_submit.slurm $numGames $agent5000 $agent15000 $evalPath/20240802_5000v15000

sbatch sh_scripts/bg_bot_evalgpu_submit.slurm $numGames $agent15000 $agent1000 $evalPath/20240802_15000v1000
sbatch sh_scripts/bg_bot_evalgpu_submit.slurm $numGames $agent15000 $agent5000 $evalPath/20240802_15000v5000
sbatch sh_scripts/bg_bot_evalgpu_submit.slurm $numGames $agent15000 $agent15000 $evalPath/20240802_15000v15000