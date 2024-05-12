#!/bin/bash
echo "DQN:"
python3 cinderella_multiple_traces_drl.py 5 50 2 5 1000 1000000 DQN
echo "QRDQN:"
python3 cinderella_multiple_traces_drl.py 5 50 2 5 1000 1000000 QRDQN