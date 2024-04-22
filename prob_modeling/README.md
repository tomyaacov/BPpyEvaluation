#### Probabilistic Model Checking (Section 5)


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
