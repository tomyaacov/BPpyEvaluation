#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_cinderella_dfs ### name of the job. replace my_job with your desired job name
#SBATCH --output run_cinderella_dfs.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=16G ### total amount of RAM // 500
#SBATCH --ntasks=1

### Start you code below ####
module load anaconda ### load anaconda module
source activate bppy-py39 ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPpyEvaluation/drl || exit

~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 50 2 5 100000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 100 2 5 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 150 2 5 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 200 2 5 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 250 2 5 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 300 2 5 1000
#
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 50 2 10 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 100 2 10 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 150 2 10 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 200 2 10 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 250 2 10 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 300 2 10 1000
#
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 50 2 15 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 100 2 15 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 150 2 15 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 200 2 15 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 250 2 15 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 300 2 15 1000
#
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 50 2 20 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 100 2 20 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 150 2 20 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 200 2 20 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 250 2 20 1000
#~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 300 2 20 1000