## Performance evaluation of SMT solvers

### Installation instructions:

 1. Create a virtual environment

`python -m venv_rich_events venv_rich_events`

 2. Activate the virtual environment

`source venv_rich_events/bin/activate`

3. Install packages

`pip install bppy`

4. Run the single-edge experiment 

`venv_rich_events/bin/python3 z3_circle_examples.py -n_0 4 -n_m 100 -s -n_e 30`

The following is a detailed explanation of each parameter.

### Running the performance evaluation

#### Meaningful parameters

`n_0` - The initial number of edges to start the experiment.  

`n_m` - The final number of edges to finish the experiment.

`n_e` - The number of times to repeat the experiment.

`s` - A flag that indicates that the experiment will be executed in a single-edge mode.

#### Examples - single edge case

1. Solving the problem starting from a regular polygon with 4 edges, until a regular polygon with 40 edges.

`venv_rich_events/bin/python3 z3_circle_examples.py -n_0 4 -n_m 40 -s`

2. Running the same experiment from example 1. for 50 times

`venv_rich_events/bin/python3 z3_circle_examples.py -n_0 4 -n_m 40 -s -n_e 50 `

#### Examples - multiple edges case

3. Solving the second problem starting from a regular polygon with 4 edges, until a regular polygon with 40 edges.

`venv_rich_events/bin/python3 z3_circle_examples.py -n_0 4 -n_m 40`

4. Running the same experiment from example 3. for 50 times

`venv_rich_events/bin/python3 z3_circle_examples.py -n_0 4 -n_m 40 -n_e 50 `

### Good Luck!
