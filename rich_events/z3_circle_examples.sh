#!/bin/bash
#SBATCH --mem=10gb
#SBATCH -c4
#SBATCH --time=2:0:0
#SBATCH --gres=gpu:1,vmem:10g
#SBATCH --error=error_log.txt
#SBATCH --output=log.txt
#SBATCH --job-name=z3_circle_examples

venv_rich_events/bin/python3 z3_circle_examples.py -n_0 1000 -n_m 1050