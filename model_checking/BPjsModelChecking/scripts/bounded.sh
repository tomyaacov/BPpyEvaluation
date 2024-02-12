#!/bin/bash

ulimit -s unlimited
export MAVEN_OPTS="-Xms1024k -Xmx16g"
mvn compile > /dev/null 2>&1
options=(
"hot_cold 30 1 true true" "hot_cold 60 1 true true" "hot_cold 90 1 true true"
"hot_cold 30 2 true true" "hot_cold 60 2 true true" "hot_cold 90 2 true true"
"hot_cold 30 3 true true" "hot_cold 60 3 true true" "hot_cold 90 3 true true"

"dining_philosophers 3 true true" "dining_philosophers 6 true true" "dining_philosophers 9 true true"

"ttt 3 3 true true"
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