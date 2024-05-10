#!/bin/bash


options=(

"hot_cold2 30 1 0" "hot_cold2 60 1 0" "hot_cold2 90 1 0"
"hot_cold2 30 2 0" "hot_cold2 60 2 0" "hot_cold2 90 2 0"
"hot_cold2 30 3 0" "hot_cold2 60 3 0" "hot_cold2 90 3 0"

"dining_philosophers2 3 0" "dining_philosophers2 6 0" "dining_philosophers2 9 0"

"ttt2 3 3 0"
)

ulimit -s unlimited

echo "option,run,time,memory" > run_all_bppy_unbounded_output.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..10}
  do
    timeout 60m time -a -o run_all_bppy_unbounded_output.csv -f "$option,$i,%E,%M" python main.py $option
    EXIT_STATUS=$?
    if [ $EXIT_STATUS -eq 124 ]
    then
    echo "$option,$i,t.o.,t.o." >> run_all_bppy_unbounded_output.csv
    else
    if [ $EXIT_STATUS -ne 0 ]
    then
    echo "$option,$i,error,$EXIT_STATUS" >> run_all_bppy_unbounded_output.csv
    fi
    fi
  done
done