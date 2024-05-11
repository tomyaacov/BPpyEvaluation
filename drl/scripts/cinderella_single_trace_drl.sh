#!/bin/bash

options=(
"5 50 2 5 1000000" "5 100 2 5 1000000" "5 150 2 5 1000000" "5 200 2 5 1000000" "5 250 2 5 1000000" "5 300 2 5 1000000"
"5 50 2 10 1000000" "5 100 2 10 1000000" "5 150 2 10 1000000" "5 200 2 10 1000000" "5 250 2 10 1000000" "5 300 2 10 1000000"
"5 50 2 15 1000000" "5 100 2 15 1000000" "5 150 2 15 1000000" "5 200 2 15 1000000" "5 250 2 15 1000000" "5 300 2 15 1000000"
"5 50 2 20 1000000" "5 100 2 20 1000000" "5 150 2 20 1000000" "5 200 2 20 1000000" "5 250 2 20 1000000" "5 300 2 20 1000000"
)

echo "option,run,time,memory" > run_single_trace_drl_output.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..10}
  do
    timeout 120m time -a -o run_single_trace_drl_output.csv -f "$option,$i,%E,%M" python3 cinderella_single_trace_drl.py $option
  done
done