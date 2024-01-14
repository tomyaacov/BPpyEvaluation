#!/bin/bash
#SBATCH --mem=32G
#SBATCH --time=120:0:0
#SBATCH --error=error_log_%j.txt
#SBATCH --output=log_%j.txt
#SBATCH --job-name=z3_circle_examples

venv_rich_events/bin/python3 z3_circle_examples.py -n_0 4 -n_m 101 -n_e 30 -s