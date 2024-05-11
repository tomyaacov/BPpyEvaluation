#### Probabilistic Model Checking (Section 5)


Each sub-directory contains a demonstration of the respective b-program evaluation for a given parameter range, in addition to the scripts used during the experiments (named modeling or sampling).
Running the demos performs the sampling followed by model translation and verification.
Note that the demo does not time-out, and as such larger parameter inputs **may take multiple days and may require additional resources**.

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

For example, running the Monty Hall experiment on a minimum of 3 and maximum of 4 doors, taking 10000 samples:
```shell
python3 monty_hall/demo.py 3 4 --samples 10000
```