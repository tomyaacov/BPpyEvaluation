#!/bin/bash
echo "DQN:"
python3 pancake_multiple_traces_drl.py 200 25 500 1000000 DQN
echo "QRDQN:"
python3 pancake_multiple_traces_drl.py 200 25 500 1000000 QRDQN