#!/bin/bash

options=(

"3 1 1 --samples 10000"
"9 2 1 --samples 10000"
"8 4 3 --samples 10000"
"10 5 2 --samples 10000"

"10 1 1 --samples 10000"
"10 2 1 --samples 10000"
"10 3 1 --samples 10000"
"10 4 1 --samples 10000"
"10 5 1 --samples 10000"
"10 6 1 --samples 10000"
"10 7 1 --samples 10000"
"10 8 1 --samples 10000"
"10 1 2 --samples 10000"
"10 2 2 --samples 10000"
"10 3 2 --samples 10000"
"10 4 2 --samples 10000"
"10 5 2 --samples 10000"
"10 6 2 --samples 10000"
"10 7 2 --samples 10000"
"10 1 3 --samples 10000"
"10 2 3 --samples 10000"
"10 3 3 --samples 10000"
"10 4 3 --samples 10000"
"10 5 3 --samples 10000"
"10 6 3 --samples 10000"
"10 1 4 --samples 10000"
"10 2 4 --samples 10000"
"10 3 4 --samples 10000"
"10 4 4 --samples 10000"
"10 5 4 --samples 10000"
"10 1 5 --samples 10000"
"10 2 5 --samples 10000"
"10 3 5 --samples 10000"
"10 4 5 --samples 10000"
"10 1 6 --samples 10000"
"10 2 6 --samples 10000"
"10 3 6 --samples 10000"

)

ulimit -s unlimited


for option in "${options[@]}"; do
  echo "$option"
  timeout 120m python3 monty/monty_demo.py $option
done