#### SMT solvers (Section 3)

The full evaluation results presented in Section 3 can be obtained by running the following commands (**this may take a few hours and may require additional resources**).

**Cinderella-Stepmother problem**

To repeat the experiment presented in Figure 1, execute the ```cinderella_experiments.py``` script with the following parameters ( **warning - this can take few minutes**):

```shell
python3 cinderella_experiments.py -n 5 -c 2 -b 25 -n_e 10
```
The ```cinderella_experiments.py``` file accepts the parameters: 
* `n` - the number of buckets.
* `c` - the number of adjacent buckets Cinderella empties.
* `b ` - The maximum number of water units a bucket can contain.
* `a` - The number of water units the stepmother pours into the buckets
* `n_e` - the number of times to repeat the experiment.

**Bit-Flip problem**

The ```bit_flipping_experiments.py``` file accepts the parameters:

 * `n` - maximal number of rows
 * `m` - maximal number of columns
 * `n_e` - The number of times to run the experiment

For instance, a scaled down evaluation of the experiment presented in Figure 2, execute the ```bit_flipping_experiments.py``` program with the following parameters:
```shell
python3 bit_flipping_experiments.py -n 3 -m 4 -n_e 10
```

To repeat the full experiment presented in Figure 2, execute the ```bit_flipping_experiments.py``` program with the following parameters (**this may take few hours and may require additional resources**):
```shell
python3 bit_flipping_experiments.py -n 4 -m 5 -n_e 10
```

**Circled Polygon problem**

The ``z3_circle_examples.py`` file accepts the parameters:
* `n_0` - the initial number of edges to start the experiment.
* `n_m` - the final number of edges to finish the experiment.
* `n_e` - the number of times to repeat the experiment.

For example, running a scaled-down evaluation of the circled-polygon experiment:
```shell
python3 z3_circle_examples.py -n_0 4 -n_m 10 -n_e 20
```

The script outputs a table with the results.

To repeat the experiment presented in Figure 4, execute the ```z3_circle_examples.py``` program with the following parameters(**this may take few hours and may require additional resources**):

```shell
python3 z3_circle_examples.py -n_0 4 -n_m 200 -n_e 30
```

