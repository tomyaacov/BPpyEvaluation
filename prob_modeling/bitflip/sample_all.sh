#!/bin/bash

options=(
"2 2 --samples 1000 -q"
"2 3 --samples 1000 -q"
"2 4 --samples 1000 -q"
"2 5 --samples 1000 -q"
"2 6 --samples 1000 -q"
"2 7 --samples 1000 -q"
"3 3 --samples 1000 -q"
"3 4 --samples 1000 -q"
"3 5 --samples 1000 -q"
"4 4 --samples 1000 -q"
"4 5 --samples 1000 -q"

)

ulimit -s unlimited

echo "Dim, Mean, SEM, Samples, Avg Time"
for option in "${options[@]}"; do
  python demo.py $option
done