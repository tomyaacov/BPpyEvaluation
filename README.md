# Artifact Submission 


**Title of the submitted paper**: Exploring and Evaluating Interplays of BPpy with Artificial Intelligence and Formal Methods

**ECOOP submission number for the paper**: 61

## Metadata 

* To run the artifact we used:
    * macOS 11.7.5 
    * Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
    * memory: 16 GB
    * disk: 256 GB

* Required hardware resources:
    * The artifact includes code for several experiments presented in the paper. Running a complete experiment in each of the evaluations takes multiple days and requires huge resources. We included instructions for a scaled-down evaluation for each experiment, which takes several minutes.

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
Inside this directory there are separate directories for each experiment discussed in the paper, as elaborated below. 

### Experiments

#### SMT solvers

The code for running the SMT solvers experiments (Section 3) is in the ``smt_solvers`` directory:

```shell
cd smt_solvers
```

The ``z3_circle_examples.py`` file accepts the parameters:
* `n_0` - the initial number of edges to start the experiment.
* `n_m` - the final number of edges to finish the experiment.
* `n_e` - the number of times to repeat the experiment.
* `s` - flag that indicates that the experiment will be executed in a single-edge mode.

For example, running a scaled-down evaluation of the single edge experiment:
```shell
python3 z3_circle_examples.py -n_0 4 -n_m 10 -s -n_e 100 -s
```

and running a scaled-down evaluation of the multi edge experiment:
```shell
python3 z3_circle_examples.py -n_0 4 -n_m 10 -n_e 20
```

The scripts outputs a table with the results presented in Figure 2 and Figure 3.

The full evaluation results presented in Section 3 can be obtained by running the following commands (**this may take a few hours and may require additional resources**):
```shell
python3 z3_circle_examples.py -n_0 4 -n_m 100 -s -n_e 30 -s
python3 z3_circle_examples.py -n_0 4 -n_m 200 -n_e 30
```


#### Symbolic Model Checking

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

The data in Table 3 concerning BPpy can be obtained by running scripts `scripts/bounded.sh` and `scripts/unbounded.sh`  (**this may take multiple days and may require additional resources**).


##### BPjs's Model Checker

```shell
cd BPjsModelChecking
```

Running the examples above using BPjs's model checker:

```shell
mvn clean compile exec:java -Dexec.args="hot_cold 30 1 true false"
```

```shell
mvn clean compile exec:java -Dexec.args="dining_philosophers 3 true true"
```

The data in Table 3 concerning BPjs can be obtained by running scripts `scripts/bounded.sh` and `scripts/unbounded.sh`  (**this may take multiple days and may require additional resources**).

#### Probabilistic Model Checking

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

The ``artifact_demonstration.py`` file runs the monty hall experiment for a single parameter configuration and accepts the parameters:
* `doors` - number of doors in total
* `prizes` - doors containing prizes
* `doors_opened` - doors opened before asking to swap
* `--samples` - number of iterations to use for sampling

For example, running the experiment for 3 doors, 1 prize, 1 door opened, and 10000 samples:
```shell
python3 artifact_demonstration.py 3 1 1 --samples 10000
```

The full evaluation results presented in Section 5 and presented in Figure 4 and Table 4 can be obtained by running the script `run_all.sh` (**this may take multiple days and may require additional resources**).


#### Deep Reinforcement Learning

The code for running the deep reinforcement lLearning experiments (Section 6) is in the ``drl`` directory:

```shell
cd drl
```

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

The full evaluation results presented in Table 5 can be obtained by running the scripts `scripts/single_trace_drl.sh` and `scripts/single_trace_search.sh` (**this may take multiple days and may require additional resources**).


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

The full evaluation results presented in Figure 5 can be obtained by running the script `multiple_traces.sh` (**this may take few hours and may require additional resources**).

#### LLM

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

The full evaluation results mentioned in the end of Section 7 can be obtained by running the script `run_all.sh`.


