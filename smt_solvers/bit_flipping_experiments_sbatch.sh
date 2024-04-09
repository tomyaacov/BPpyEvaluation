#!/bin/bash
#SBATCH --mem=64G
#SBATCH --time=120:0:0
#SBATCH --error=error_log_%j.txt
#SBATCH --output=log_%j.txt
#SBATCH --job-name=bit_flipping_experiments

venv_rich_events/bin/python3 bit_flipping_experiments.py -n 10 -m 10 -n_e 10