#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_multiple_traces_dqn_200_25_2 ### name of the job. replace my_job with your desired job name
#SBATCH --output run_multiple_traces_dqn_200_25_2.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=32G ### total amount of RAM // 500
#SBATCH --ntasks=1
#SBATCH --gpus=1

### Start you code below ####
module load anaconda ### load anaconda module
source activate BPpyLiveness ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPpyEvaluation/drl || exit

~/.conda/envs/BPpyLiveness/bin/python pancake_multiple_traces_drl.py 200 25 500 2000000 DQN