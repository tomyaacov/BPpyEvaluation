#!/bin/bash


options=(
"5 50 2 5" "5 100 2 5" "5 150 2 5" "5 200 2 5" "5 250 2 5" "5 300 2 5"
"5 50 2 10" "5 100 2 10" "5 150 2 10" "5 200 2 10" "5 250 2 10" "5 300 2 10"
"5 50 2 15" "5 100 2 15" "5 150 2 15" "5 200 2 15" "5 250 2 15" "5 300 2 15"
"5 50 2 20" "5 100 2 20" "5 150 2 20" "5 200 2 20" "5 250 2 20" "5 300 2 20"
)

echo "option,run,time,memory" > run_single_trace_search_output.csv
for option in "${options[@]}"; do
  echo "$option"
  for i in {1..10}
  do
    timeout 120m time -a -o run_single_trace_search_output.csv -f "$option,$i,%E,%M" python3 cinderella_single_trace_search.py $option
  done
done