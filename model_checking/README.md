#### Symbolic Model Checking (Section 4)

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

The data in Table 3 concerning BPpy can be obtained by running scripts (**this may take multiple days and may require additional resources**):
* `scripts/bounded.sh` - the script will create a csv file `run_all_bppy_bounded_output.csv` with the results of the time and memory of BPpy's bounded model checking.
* `scripts/unbounded.sh` - the script will create a csv file `run_all_bppy_unbounded_output.csv` with the results of the time and memory of BPpy's unbounded model checking.


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

The data in Table 3 concerning BPjs can be obtained by running scripts (**this may take multiple days and may require additional resources**):
* `scripts/bounded.sh` - the script will create a csv file `run_all_bpjs_bounded_output.csv` with the results of the time and memory of BPjs's bounded model checking.
* `scripts/unbounded.sh` - the script will create a csv file `run_all_bpjs_unbounded_output.csv` with the results of the time and memory of BPjs's unbounded model checking.

