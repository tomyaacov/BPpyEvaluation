#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_cinderella_single_trace_drl ### name of the job. replace my_job with your desired job name
#SBATCH --output run_cinderella_single_trace_drl.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=32G ### total amount of RAM // 500
#SBATCH --ntasks=1
#SBATCH --gpus=1

### Start you code below ####
module load anaconda ### load anaconda module
source activate BPpyLiveness ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPpyEvaluation/drl || exit

#options = ()
#options=(
#"4 8 2 5" "5 10 2 5" "6 12 2 5" "7 14 2 5"
#"4 8 2 6" "5 10 2 6" "6 12 2 6" "7 14 2 6"
#"4 8 2 7" "5 10 2 7" "6 12 2 7" "7 14 2 7"
#)
#options=(
#"4 8 2 5 1000000" "5 10 2 5 1000000" "6 12 2 5 1000000" "7 14 2 5 1000000"
#"4 8 2 6 1000000" "5 10 2 6 1000000" "6 12 2 6 1000000" "7 14 2 6 1000000"
#"4 8 2 7 1000000" "5 10 2 7 1000000" "6 12 2 7 1000000" "7 14 2 7 1000000"
#)
options=(
"5 50 2 5 1000000" "5 100 2 5 1000000" "5 150 2 5 1000000" "5 200 2 5 1000000" "5 250 2 5 1000000" "5 300 2 5 1000000"
"5 50 2 10 1000000" "5 100 2 10 1000000" "5 150 2 10 1000000" "5 200 2 10 1000000" "5 250 2 10 1000000" "5 300 2 10 1000000"
"5 50 2 15 1000000" "5 100 2 15 1000000" "5 150 2 15 1000000" "5 200 2 15 1000000" "5 250 2 15 1000000" "5 300 2 15 1000000"
"5 50 2 20 1000000" "5 100 2 20 1000000" "5 150 2 20 1000000" "5 200 2 20 1000000" "5 250 2 20 1000000" "5 300 2 20 1000000"
)

echo "option,run,time,memory" > run_cinderella_single_trace_drl_output.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..30}
  do
    timeout 120m /usr/bin/time -a -o run_cinderella_single_trace_drl_output.csv -f "$option,$i,%E,%M" ~/.conda/envs/BPpyLiveness/bin/python cinderella_single_trace_drl.py $option $i
  done
done