#### Probabilistic Model Checking (Section 5)

The code for running the probabilistic model checking experiments (Section 5) is in the three subdirectories of ``prob_modeling``:

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


``monty_demo.py`` accepts the parameters:
* `doors` - number of doors in total
* `prizes` - doors containing prizes
* `doors_opened` - doors opened before asking to swap
* `--samples` - number of iterations to use for sampling

For example, running the experiment for 3 doors, 1 prize, 1 door opened, and 10000 samples:
```shell
python3 artifact_demonstration.py 3 1 1 --samples 10000
```

``dice_demo.py`` accepts the parameters:
* `sides` - number of sides in the simulated dice
* `--samples` - number of iterations to use for sampling


``bitflip_demo.py`` accepts the parameters:
* `n` - number of rows in the matrix
* `m` - number of columns in the matrix
* `--samples` - number of iterations to use for sampling

Note the bitflip demo does not generate the translated models for exact analysis. 
