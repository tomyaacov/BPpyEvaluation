#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_main ### name of the job. replace my_job with your desired job name
#SBATCH --output run_main.out ### output log for running job - %J is the job number variable
##SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
##SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=32G ### total amount of RAM // 500
#SBATCH --ntasks=1
#SBATCH --gpus=1

### Start you code below ####

out_file_name="output/"
while [ $# -gt 0 ]; do
    if [[ $1 == "--"* ]]; then
        v="${1/--/}"
        declare "$v"="$2"
        out_file_name="$out_file_name""$v"_"$2"_
        shift
    fi
    shift
done


module load anaconda ### load anaconda module
source activate BPpyLiveness ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPpyLiveness/ || exit
/usr/bin/time -a -o $out_file_name -f "time:%E,memory:%M" ~/.conda/envs/BPpyLiveness/bin/python main_mask.py --n $n --k $k --m $m --total_timesteps $total_timesteps --state_mode $state_mode --reward_mode $reward_mode > $out_file_name