#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_pancake_dfs ### name of the job. replace my_job with your desired job name
#SBATCH --output run_pancake_dfs.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=32G ### total amount of RAM // 500
#SBATCH --ntasks=1

### Start you code below ####

out_file_name="output/dfs_results"


module load anaconda ### load anaconda module
source activate BPpyLiveness ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPpyEvaluation/drl || exit

~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 50 --m 5
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 100 --m 5
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 150 --m 5
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 200 --m 5
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 250 --m 5
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 300 --m 5

~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 50 --m 10
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 100 --m 10
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 150 --m 10
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 200 --m 10
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 250 --m 10
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 300 --m 10

~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 50 --m 15
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 100 --m 15
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 150 --m 15
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 200 --m 15
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 250 --m 15
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 300 --m 15

~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 50 --m 20
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 100 --m 20
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 150 --m 20
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 200 --m 20
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 250 --m 20
~/.conda/envs/BPpyLiveness/bin/python pancake_dfs.py --n 300 --m 20
