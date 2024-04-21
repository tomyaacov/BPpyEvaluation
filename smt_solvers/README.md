
### Experiments

#### SMT solvers (Section 3)

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
python3 z3_circle_examples.py -n_0 4 -n_m 10 -s -n_e 20 -s
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
