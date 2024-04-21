
### Experiments

#### SMT solvers (Section 3)

The code for running the SMT solvers experiments (Section 3) is in the ``smt_solvers`` directory:

```shell
cd smt_solvers
```
The full evaluation results presented in Section 3 can be obtained by running the following commands (**this may take a few hours and may require additional resources**).

**Cinderella-Stepmother problem**

To repeat the experiment presented in the paper you need to execute the ```cinderella_experiments.py``` program with the following parameters:

```shell
python cinderella_experiments.py -n 5 -c 2 -b 25 -n_e 10
```
The ```cinderella_experiments.py``` file accepts the parameters: 
* `n` - the number of buckets.
* `c` - the number of adjacent buckets Cinderella empties.
* `b ` - The maximum number of water units a bucket can contain.
* `a` - The number of water units the stepmother pours into the buckets
* `n_e` - the number of times to repeat the experiment.

**Bit-Flip problem**

To repeat the experiment presented in the paper you need to execute the ```bit_flipping_experiments.py``` program with the following parameters:
```shell
python bit_flipping_experiments.py -n 4 -m 5 -n_e 10
```
The ```bit_flipping_experiments.py``` file accepts the parameters:

 * `n` - the number of rows
 * `m` - the number of columns
 * `n_e` - The number of times to run the experiment

**Circled Polygon problem**

The ``z3_circle_examples.py`` file accepts the parameters:
* `n_0` - the initial number of edges to start the experiment.
* `n_m` - the final number of edges to finish the experiment.
* `n_e` - the number of times to repeat the experiment.
* `s` - flag that indicates that the experiment will be executed in a single-edge mode.

For example, running a scaled-down evaluation of the circled-polygon experiment:
```shell
python3 z3_circle_examples.py -n_0 4 -n_m 10 -n_e 20
```

The script outputs a table with the results.

To repeat the experiment presented in the paper you need to execute the ```z3_circle_examples.py``` program with the following parameters:

```shell
python z3_circle_examples.py -n_0 4 -n_m 200 -n_e 30
```

Good luck!
