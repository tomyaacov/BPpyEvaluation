#!/bin/bash

options=(

"r1"
"r2"
"r3"
"r4"
"r5"
"r6"
"r7"
"r8"
"r9"
"r10"
"rs1"
"rs2"
"rs3"
"rs4"
"rs5"
"rs6"
"rs7"
"rs8"
"rs9"
"rs10"


)

echo "BPpy"
for option in "${options[@]}"; do
  echo "$option"
  python3 main_bppy.py $option
done

echo "Regular Python"
for option in "${options[@]}"; do
  echo "$option"
  python3 main_regular.py $option
done