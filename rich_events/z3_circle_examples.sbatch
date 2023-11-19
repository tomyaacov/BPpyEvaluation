#!/bin/bash
#SBATCH --mem=4G
#SBATCH --time=24:0:0
#SBATCH --error=error_log.txt
#SBATCH --output=log.txt
#SBATCH --job-name=z3_circle_examples

venv_rich_events/bin/python3 z3_circle_examples.py -n_0 4 -n_m 200 -n_e 30