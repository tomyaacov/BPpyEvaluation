# Artifact Submission 

**Title of the submitted paper**: Exploring and Evaluating Interplays of BPpy with Artificial Intelligence and Formal Methods

**ECOOP submission number for the paper**: 134

## Metadata 

* To run the artifact we used:
    * macOS 11.7.5 
    * Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
    * memory: 16 GB
    * disk: 256 GB

* Required hardware resources:
    * The artifact includes code for all experiments presented in the paper. Running a complete experiment in each of the evaluations takes multiple days and requires huge resources. We included instructions for a scaled-down evaluation for each experiment, which takes several minutes.

* Known compatibility issues of the container:
    * No compatibility issues are known.

* Claimed badges:
  * Functional
  * Reusable
  * Available

## Installation and Usage

The artifact contains all experiments contained in the paper.

To run all experiments, the first step is to pull the docker image and run it:
```shell
docker pull annonymouswriter/bp-evaluation:latest
docker run -it annonymouswriter/bp-evaluation:latest
```
When running the container, the current directory will be ``BPpyEvaluation``.

Inside the ``BPpyEvaluation`` directory there are separate directories for each experiment discussed in the paper, as elaborated below. 

### Experiments

#### SMT solvers (Section 3)

The code for running the SMT solvers experiments (Section 3) is in the ``smt_solvers`` directory:

```shell
cd smt_solvers
```

**Cinderella-Stepmother problem**

The ```cinderella_experiments.py``` file accepts the parameters: 
* `n` - the number of buckets.
* `c` - the number of adjacent buckets Cinderella empties.
* `b ` - The maximum number of water units a bucket can contain.
* `a` - The number of water units the stepmother pours into the buckets
* `n_e` - the number of times to repeat the experiment.

For instance, a scaled down evaluation of the experiment presented in Figure 1, execute the ```cinderella_experiments.py``` program with the following parameters:
```shell
python3 cinderella_experiments.py -n 5 -c 2 -b 10 -n_e 3
```

To repeat the experiment presented in Figure 1, execute the ```cinderella_experiments.py``` script with the following parameters (**this may take few hours and may require additional resources**):

```shell
python3 cinderella_experiments.py -n 5 -c 2 -b 25 -n_e 10
```

The script outputs a table with the results presented in Figure 1.

**Bit-Flip problem**

The ```bit_flipping_experiments.py``` file accepts the parameters:

 * `n` - maximal number of rows
 * `m` - maximal number of columns
 * `n_e` - The number of times to run the experiment

For instance, a scaled down evaluation of the experiment presented in Figure 2, execute the ```bit_flipping_experiments.py``` program with the following parameters:
```shell
python3 bit_flipping_experiments.py -n 3 -m 4 -n_e 5
```

To repeat the full experiment presented in Figure 2, execute the ```bit_flipping_experiments.py``` program with the following parameters (**this may take few hours and may require additional resources**):
```shell
python3 bit_flipping_experiments.py -n 4 -m 5 -n_e 10
```

The script outputs a table with the results presented in Figure 2.

**Circled Polygon problem**

The ``z3_circle_examples.py`` file accepts the parameters:
* `n_0` - the initial number of edges to start the experiment.
* `n_m` - the final number of edges to finish the experiment.
* `n_e` - the number of times to repeat the experiment.

For example, running a scaled-down evaluation of the circled-polygon experiment:
```shell
python3 z3_circle_examples.py -n_0 4 -n_m 10 -n_e 20
```


To repeat the experiment presented in Figure 4, execute the ```z3_circle_examples.py``` program with the following parameters(**this may take few hours and may require additional resources**):

```shell
python3 z3_circle_examples.py -n_0 4 -n_m 200 -n_e 30
```

The script outputs a table with the results presented in Figure 4.

#### Symbolic Model Checking (Section 4)

The code for running the symbolic model checking experiments (Section 4) are in the ``model_checking`` directory:

```shell
cd model_checking
```

The folder contains two subfolders: `BPpyModelChecker` for the BPpy's symbolic model checker experiments and `BPjsModelChecking` for running BPjs's model checker.

##### BPpy's Symbolic Model Checker

```shell
cd BPpyModelChecker
```

The ``main.py`` file accepts the following parameters:
* example - one of: `hot_cold2`,`dining_philosophers2`,`ttt2`
* two problem parameters - `n` and `m`
* bounded mc - `1` for true and `0` otherwise

For example, running *unbounded* symbolic model checking for the hot cold example with n=30 and m=1:
```shell
python3 main.py hot_cold2 30 1 0
```

and running *bounded* symbolic model checking for the dining philosophers example with n=3:
```shell
python3 main.py dining_philosophers2 3 1 1
```

The data in Table 3 concerning BPpy can be obtained by running the following scripts using the `bash` command (**this may take multiple days and may require additional resources**):
* `scripts/bounded.sh` - the script will create a csv file `run_all_bppy_bounded_output.csv` with the results of the time and memory of BPpy's bounded model checking.
* `scripts/unbounded.sh` - the script will create a csv file `run_all_bppy_unbounded_output.csv` with the results of the time and memory of BPpy's unbounded model checking.


##### BPjs's Model Checker

```shell
cd BPjsModelChecking
```

Running the examples above using BPjs's model checker:

```shell
mvn exec:java -Dexec.args="hot_cold 30 1 true false"
```

```shell
mvn exec:java -Dexec.args="dining_philosophers 3 true true"
```

The data in Table 3 concerning BPjs can be obtained by running the following scripts using the `bash` command (**this may take multiple days and may require additional resources**):
* `scripts/bounded.sh` - the script will create a csv file `run_all_bpjs_bounded_output.csv` with the results of the time and memory of BPjs's bounded model checking.
* `scripts/unbounded.sh` - the script will create a csv file `run_all_bpjs_unbounded_output.csv` with the results of the time and memory of BPjs's unbounded model checking.

#### Probabilistic Model Checking (Section 5)

The code for running the probabilistic model checking experiments (Section 5) is in the ``prob_modeling`` directory:

```shell
cd prob_modeling
```

Running the experiments requires an initial step of downloading and installing the prism model checker inside the ``prob_modeling`` directory:

```shell
curl https://www.prismmodelchecker.org/dl/prism-4.8-linux64-x86.tar.gz -o prism-4.8-linux64-x86.tar.gz
gunzip prism-4.8-linux64-x86.tar.gz
tar -xf prism-4.8-linux64-x86.tar
cd prism-4.8-linux64-x86
./install.sh
cd ..
```

Each sub-directory contains a demonstration of the respective b-program for a given parameter configuration, in addition to the scripts used during the experiments (named modeling or sampling).
The scripts should be run from the directory in which the above installation was performed.

##### Monty Hall Problem

``monty/monty_demo.py`` accepts the parameters:
* `doors` - number of doors in total
* `prizes` - doors containing prizes
* `doors_opened` - doors opened before asking to swap
* `--samples` - number of iterations to use for sampling

For example, running the experiment for 3 doors, 1 prize, 1 door opened, and 10000 samples:
```shell
python3 monty/monty_demo.py 3 1 1 --samples 10000
```

The full evaluation results presented in Section 5 and presented in Figure 5 and Table 4 can be obtained by running the script `monty/run_all.sh` (**this may take multiple days and may require additional resources**).


##### Dice 

``dice/dice_demo.py`` accepts the parameters:
* `sides` - number of sides in the simulated dice
* `--samples` - number of iterations to use for sampling

For example, running the experiment for a dice with 6 sides and 10000 samples:
```shell
python3 dice/dice_demo.py 6 --samples 10000
```

##### Bit Flip

``bitflip/bitflip_demo.py`` accepts the parameters:
* `n` - number of rows in the matrix
* `m` - number of columns in the matrix
* `--samples` - number of iterations to use for sampling

For example, running the experiment for a 3x3 matrix and 1000 samples:
```shell
python3 bitflip/bitflip_demo.py 3 3 --samples 1000
```

**Note the bitflip demo does not generate the translated models for exact analysis.**


#### Deep Reinforcement Learning (Section 6)

The code for running the deep reinforcement learning experiments (Section 6) is in the ``drl`` directory:

```shell
cd drl
```

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

The full evaluation results presented in Table 9 can be obtained by running the following scripts using the `bash` command (**this may take multiple days and may require additional resources**): 
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
This is a reduced evaluation which outputs a table with the results presented in Figure 10.

The full evaluation results presented in Figure 10 can be obtained by running the script `scripts/multiple_traces.sh` using the `bash` command (**this may take few hours and may require additional resources**).

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
can be obtained by running the following scripts using the `bash` command:
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
can be obtained by running the script `scripts/cinderella_multiple_traces.sh`  using the `bash` command (**this may take few hours and may require additional resources**).

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

#### LLM (Section 8)

The code for running the LLM experiments (Section 7) is in the ``llm`` directory:

```shell
cd llm
```

The ``main_bppy.py`` file runs the evaluation for the BP model, and the ``main_regular.py`` runs the evaluation for the python model.
Both accept a single parameter, an example identifier, one of `r1,...,r10` or `rs1,...,rs10`


For example, running the evaluation of the BP model for the specification example `rs1`:
```shell
python3 main_bppy.py rs1
```

and running the evaluation of the Python model for the specification example `rs1`:
```shell
python3 main_regular.py rs1
```

The scripts output the alignment of the 100 sampled traces with requirements.

The full evaluation results mentioned in the end of Section 8 can be obtained by running the script `run_all.sh` using the `bash` command.

## Additional Information Regarding Claimed Badges

### Available

During the review process, the artifact is available at [https://figshare.com/s/6635a52bad0d1a2781e8](https://figshare.com/s/6635a52bad0d1a2781e8).
It can be published under a Creative Commons license.

### Functional and Reusable

All experimental claims are referenced in their relevant subsection above (divided to paper sections). 
Each reference includes instructions on how to run the full experiment and obtain the results presented in the paper.

The artifact implements several integration for the BPpy package. Users can reuse the artifact when using these integrations to other b-programs they implement. 

The artifact and its dependencies are open-source.