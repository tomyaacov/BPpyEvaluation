#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_single_trace_search2 ### name of the job. replace my_job with your desired job name
#SBATCH --output run_single_trace_search2.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=32G ### total amount of RAM // 500
#SBATCH --ntasks=1

### Start you code below ####
module load anaconda ### load anaconda module
source activate BPpyLiveness ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPpyEvaluation/drl || exit

#options = ()
options=(
"200 25" "200 50" "200 75" "200 100"
"300 25" "300 50" "300 75" "300 100"
"400 25" "400 50" "400 75" "400 100"
"500 25" "500 50" "500 75" "500 100"
)

echo "option,run,time,memory" > run_single_trace_search_output2.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..5}
  do
    timeout 60m /usr/bin/time -a -o run_single_trace_search_output2.csv -f "$option,$i,%E,%M" python pancake_single_trace_search.py $option
  done
done