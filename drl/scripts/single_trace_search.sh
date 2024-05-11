#!/bin/bash


options=(
"200 25" "200 50" "200 75" "200 100"
"300 25" "300 50" "300 75" "300 100"
"400 25" "400 50" "400 75" "400 100"
"500 25" "500 50" "500 75" "500 100"
)

echo "option,run,time,memory" > run_single_trace_search_output.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..10}
  do
    timeout 120m time -a -o run_single_trace_search_output.csv -f "$option,$i,%E,%M" python3 pancake_single_trace_search.py $option
  done
done