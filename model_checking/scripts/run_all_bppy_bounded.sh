#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_all_bppy_bounded ### name of the job. replace my_job with your desired job name
#SBATCH --output run_all_bppy_bounded.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=16G ### total amount of RAM // 500
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32 ##. // max 128

### Start you code below ####
module load anaconda ### load anaconda module
source activate bppy_model_checking ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPpyModelChecker/ || exit
ulimit -s unlimited
#options = ()
options=(

"hot_cold2 30 1 1" "hot_cold2 60 1 1" "hot_cold2 90 1 1"
"hot_cold2 30 2 1" "hot_cold2 60 2 1" "hot_cold2 90 2 1"
"hot_cold2 30 3 1" "hot_cold2 60 3 1" "hot_cold2 90 3 1"

"dining_philosophers2 3 1" "dining_philosophers2 6 1" "dining_philosophers2 9 1" "dining_philosophers2 12 1" "dining_philosophers2 15 1"

"ttt2 2 2 1" "ttt2 3 3 1" "ttt2 4 4 1"
)
echo "option,run,time,memory" > run_all_bppy_bounded_output.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..5}
  do
    timeout 30m /usr/bin/time -a -o run_all_bppy_bounded_output.csv -f "$option,$i,%E,%M" python main.py $option
    EXIT_STATUS=$?
    if [ $EXIT_STATUS -eq 124 ]
    then
    echo "$option,$i,t.o.,t.o." >> run_all_bppy_bounded_output.csv
    else
    if [ $EXIT_STATUS -ne 0 ]
    then
    echo "$option,$i,error,$EXIT_STATUS" >> run_all_bppy_bounded_output.csv
    fi
    fi
  done
done