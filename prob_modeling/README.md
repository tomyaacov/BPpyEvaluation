#### Probabilistic Model Checking (Section 5)


Each sub-directory contains a demonstration of the respective b-program evaluation for a given parameter range, in addition to the scripts used during the experiments (named modeling or sampling).
Running the demos performs the sampling followed by model translation and verification.

##### Monty Hall

The code for the monty hall experiment is located in the `monty_hall` directory. 
The demo must be run from within the `monty_hall` directory:

`demo.py` accepts the following parameters:
* `min` - the minimum number of doors
* `max` - the maximum number of doors
* `--samples` - the number of samples taken

For example, running the Monty Hall experiment on a minimum of 3 and maximum of 4 doors, taking 10000 samples:
```shell
python3 demo.py 3 4 --samples 10000
```

The script outputs the sampling results to different csv files the `samples` subdirectory.
For instance, the results of the above command reproduce the one shown in Figure 5(a), 
and are saved to `samples/sample_3d1p1o.csv`.

The above command also produces the results for the analysis shown in Table 4, 
which are saved to `translation_overview.csv` (albeit with different parameters). 
Larger parameters inputs, shown in Table 4, may take multiple days and require additional resources.
Note that since the demo script does not timeout, a scaled down evaluation can instead be achieved by running the following command (**this can take few minutes**):
```shell
python3 demo.py 7 7 --samples 10000
```

##### Dice Problem



##### Bitflip




To get the results in Figure 5 run the following commands:
```shell
```
the results will based saved to kdgldfg.csv

To get the results in Table 4 run the following commands:
```shell

```
the results will be saved to translation.



##### Directory structure
The directories largely share the same structure and usage:

* `bprogram_name.py` - contains the b-program and respective parameter(s) generation
* `demo.py` - python program for performing the evaluation on parmeters within the given arguments range
* `sampling.py` - generates samples and statistics
* `modeling.py` - generates the b-program PRISM translation and respective propositions
* `run_computation.sh` - runs Storm on the translations + propositions within the models subdirectory
* `read_log.py` - processes the above's results into one table 

**Note the bitflip demo does not generate the translated models for exact analysis.**


|                  | **Parameter**      | **Min** | **Max** |
|------------------|--------------------|---------|---------|
| **Monty Hall**   | Total doors        | 3       | 10      |
| **Dice Problem** | Number of sides    | 6       | 35      |
| **Bitflip**      | Matrix  dimensions | 2,2     | 4,5     |
