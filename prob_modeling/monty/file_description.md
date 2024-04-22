## Probalistic Modeling in BPpy

  
  
 

File breakdown:
- `bppy_converter_benchmark.ipynb` - Full demo of sampling and model translation + checking of the Monty Hall 2.0 problem seen in the paper. Model verification is done in PRISM instead of Storm as the more portable option.
- `bppy_modeling.py` - Used to generate all the PRISM and property files.
- `bppy_sampling.py` - Used to run the sampling.
- `modeling_verification_overview.csv` - Translation, check time and probability result for each parameter combination. 
- `run_model.sh` - Batch run Storm on the PRISM and property files.
- `sample_take_plot_res.py` - Reduces the resolution of the sampling results to something Overleaf could handle.
- `storm_read_log.py` - Extracts the model translation and check times from generated logs.
- `translation_times.ipynb` - Data plotting and generation drafts.