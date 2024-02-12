#!/bin/bash

options=(
"200 25 100000" "200 50 100000" "200 75 100000" "200 100 100000"
"300 25 100000" "300 50 100000" "300 75 100000" "300 100 100000"
"400 25 100000" "400 50 100000" "400 75 100000" "400 100 100000"
"500 25 100000" "500 50 100000" "500 75 100000" "500 100 100000"
)

echo "option,run,time,memory" > run_single_trace_drl_output.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..10}
  do
    timeout 120m /usr/bin/time -a -o run_single_trace_drl_output.csv -f "$option,$i,%E,%M" python3 pancake_single_trace_drl.py $option
  done
done