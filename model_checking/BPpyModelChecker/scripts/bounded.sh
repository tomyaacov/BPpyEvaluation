#!/bin/bash

options=(

"hot_cold2 30 1 1" "hot_cold2 60 1 1" "hot_cold2 90 1 1"
"hot_cold2 30 2 1" "hot_cold2 60 2 1" "hot_cold2 90 2 1"
"hot_cold2 30 3 1" "hot_cold2 60 3 1" "hot_cold2 90 3 1"

"dining_philosophers2 3 1" "dining_philosophers2 6 1" "dining_philosophers2 9 1"

"ttt2 3 3 1"
)

ulimit -s unlimited

echo "option,run,time,memory" > run_all_bppy_bounded_output.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..10}
  do
    timeout 60m /usr/bin/time -a -o run_all_bppy_bounded_output.csv -f "$option,$i,%E,%M" python3 main.py $option
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