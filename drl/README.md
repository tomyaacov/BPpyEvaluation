#### Deep Reinforcement Learning (Section 6)

##### Pancake example

The ``pancake_single_trace_drl.py`` file contain the experiment of finding a single valid trace using DRL. 
It accepts the parameters:
* `n` - number of pancakes in the example
* `b` - thickness bound
* learning rounds for the DRL algorithm.


For example, running ``pancake_single_trace_drl.py`` for `n=200`, `b=25`:
```shell
python3 pancake_single_trace_drl.py 200 25 100000
```

The ``pancake_single_trace_search.py`` file contain the experiment of finding a single valid trace using search. 
It accepts the parameters:
* `n` - number of pancakes in the example
* `b` - thickness bound


For example, running ``pancake_single_trace_search.py`` for `n=200`, `b=25` - **warning - this can take few minutes**
```shell
python3 pancake_single_trace_search.py 200 25
```

The full evaluation results presented in Table 9 can be obtained by running the scripts (**this may take multiple days and may require additional resources**): 
* `scripts/single_trace_drl.sh` - the script will create a csv file, `run_single_trace_drl_output.csv`, with the memory and time of the DRL algorithm in the table.
* `scripts/single_trace_search.sh` - the script will create a csv file, `run_single_trace_search_output.csv`, with the memory and time of the search algorithm in the table.


The ``pancake_multiple_traces_drl.py`` file contain the experiment of finding a valid non-deterministic policy for the pancake example.
It accepts the following parameters:
* `n` - number of pancakes in the example
* `b` - thickness bound
* number of evaluated traces
* learning rounds for the DRL algorithm
* algorithm used - on of `DQN`,`QRDQN`


For example, running ``pancake_multiple_traces_drl.py`` for `n=200`, `b=25` - **warning - this can take few minutes**
```shell
python3 pancake_multiple_traces_drl.py 200 25 500 100000 DQN
```
This is a reduced evaluation which outputs a table with the results presented in Figure 5.

The full evaluation results presented in Figure 10 can be obtained by running the script `scripts/multiple_traces.sh` (**this may take few hours and may require additional resources**).

##### Cinderella-Stepmother example

The ``cinderella_single_trace_drl.py`` file contain the experiment of finding a single valid trace using DRL. 
It accepts the parameters:

* `A` - the number water units Cinderella’s stepmother distributes across the buckets in each round
* `B` - capacity of each bucket
* `C` - number of adjacent buckets that Cinderella empties in each round
* `N` - number of buckets
* `STEPS` - number of learning rounds

For example, running ``cinderella_single_trace_drl.py`` for `A=5`, `B=50`, `C=2`, and `N=5`:
```shell
python3 cinderella_single_trace_drl.py 5 50 2 5 1000000
```

The ``cinderella_single_trace_search.py`` file contain the experiment of finding a single valid trace using search. 
It accepts the parameters:

* `A` - the number water units Cinderella’s stepmother distributes across the buckets in each round
* `B` - capacity of each bucket
* `C` - number of adjacent buckets that Cinderella empties in each round
* `N` - number of buckets

For example, running ``cinderella_single_trace_drl.py`` for `A=5`, `B=50`, `C=2`, and `N=5`:
```shell
python3 cinderella_single_trace_search.py 5 50 2 5
```

The full evaluation results presented in the appendix "Cinderella-Stepmother Problem DRL Results"  (**this may take multiple days and may require additional resources**): 
can be obtained by running the scripts:
* `scripts/cinderella_single_trace_drl.sh` - the script will create a csv file, `run_single_trace_drl_output.csv`, with the memory and time of the DRL algorithm in the table.
* `scripts/cinderella_single_trace_search.sh`. - the script will create a csv file, `run_single_trace_search_output.csv`, with the memory and time of the search algorithm in the table.


The ``cinderella_multiple_traces_drl.py`` file contain the experiment of finding a single valid trace using search. 
It accepts the parameters:
* `A` - the number water units Cinderella’s stepmother distributes across the buckets in each round
* `B` - capacity of each bucket
* `C` - number of adjacent buckets that Cinderella empties in each round
* `N` - number of buckets
* number of evaluated traces
* learning rounds for the DRL algorithm
* algorithm used - on of `DQN`,`QRDQN`


For example, running ``cinderella_multiple_traces_drl.py`` for `A=5`, `B=50`, `C=2`, and `N=5` - **warning - this can take few minutes**
```shell
python3 cinderella_multiple_traces_drl.py 5 50 2 5 1000 100000 "DQN"
```
The full evaluation results presented in the appendix "Cinderella-Stepmother Problem DRL Results" 
can be obtained by running the script `scripts/cinderella_multiple_traces.sh` (**this may take few hours and may require additional resources**).

#### (DRL + Probabilities + SMT Solvers) (Section 7)

The ``bit_flipping.py`` file contain the experiment presented in Section 7.
It accepts the parameters:
* `N` - number of matrix rows
* `M` - number of matrix columns
* learning rounds for the DRL algorithm.

For example, running ``bit_flipping.py`` for `N=3`, `M=3` (**this may take few hours and may require additional resources**):
```shell
python3 bit_flipping.py 3 3 100000
```

The script saves the results presented in the evaluation in a csv file. 
For instance, the results for the command above will be saved in `output/33100000/results.csv`.

The full evaluation results presented in Figure 11 can be obtained by running the script `scripts/bit_flip_all.sh` using the `bash` command (**this may take few hours and may require additional resources**).

To compute the random and greedy baselines, run the ``bit_flip_random.py`` that accepts the parameters:
* `N` - number of matrix rows
* `M` - number of matrix columns
* greedy or random (1 for greedy, 0 for random)
* number of samples

For example (**this may take few minutes**):
```shell
python3 bit_flip_random.py 3 3 1 1000
```