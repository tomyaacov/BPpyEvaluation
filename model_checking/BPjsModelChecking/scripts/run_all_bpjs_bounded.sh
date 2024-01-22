#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_all_bpjs_bounded ### name of the job. replace my_job with your desired job name
#SBATCH --output run_all_bpjs_bounded.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=32G ### total amount of RAM // 500
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32 ##. // max 128

### Start you code below ####
module load anaconda ### load anaconda module
source activate bppy_model_checking ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPjsModelChecking/ || exit
ulimit -s unlimited
export MAVEN_OPTS="-Xms1024k -Xmx16g"
mvn compile > /dev/null 2>&1
options=(
"hot_cold 30 1 true true" "hot_cold 60 1 true true" "hot_cold 90 1 true true"
"hot_cold 30 2 true true" "hot_cold 60 2 true true" "hot_cold 90 2 true true"
"hot_cold 30 3 true true" "hot_cold 60 3 true true" "hot_cold 90 3 true true"

"dining_philosophers 3 true true" "dining_philosophers 6 true true" "dining_philosophers 9 true true" "dining_philosophers 12 true true"

"ttt 3 3 true true" "ttt 4 4 true true"
)

echo "option,run,time,memory" > run_all_bpjs_bounded_output.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..10}
  do
    timeout 60m /usr/bin/time -a -o run_all_bpjs_bounded_output.csv -f "$option,$i,%E,%M" mvn exec:java -D"exec.args"="$option"
    EXIT_STATUS=$?
    if [ $EXIT_STATUS -eq 124 ]
    then
    echo "$option,$i,t.o.,t.o." >> run_all_bpjs_bounded_output.csv
    else
    if [ $EXIT_STATUS -ne 0 ]
    then
    echo "$option,$i,error,$EXIT_STATUS" >> run_all_bpjs_bounded_output.csv
    fi
    fi
  done
done