#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_cinderella_dfs ### name of the job. replace my_job with your desired job name
#SBATCH --output run_cinderella_dfs.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=32G ### total amount of RAM // 500
#SBATCH --ntasks=1

### Start you code below ####
module load anaconda ### load anaconda module
source activate bppy-py39 ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPpyEvaluation/drl || exit

~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 10 2 5 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 15 2 5 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 20 2 5 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 25 2 5 1000

~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 10 2 6 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 15 2 6 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 20 2 6 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 25 2 6 1000

~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 10 2 7 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 15 2 7 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 20 2 7 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 25 2 7 1000

~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 10 2 8 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 15 2 8 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 20 2 8 1000
~/.conda/envs/bppy-py39/bin/python cinderella_dfs.py 5 25 2 8 1000