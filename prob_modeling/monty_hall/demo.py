import argparse, os, shutil, subprocess
import numpy as np
import monty

from sampling import sample_params
from modeling import run_translation
from read_log import process_files

# cleans existing directories
CWD = os.path.dirname(os.path.realpath(__file__))
dir_samples = CWD + '/samples'
dir_models = CWD + '/models'
if os.path.exists(dir_samples):
    shutil.rmtree(dir_samples)
os.makedirs(dir_samples)
dir_models = CWD + '/models'
if os.path.exists(dir_models):
    shutil.rmtree(dir_models)
os.makedirs(dir_models)

parser = argparse.ArgumentParser(
	description='BPpy Monty Hall problem solving demonstation. Runs sampling and translation + model checking of a given parameter range.')
parser.add_argument('min', type=int, metavar='min_doors', default=3,
					choices=range(3, 10), help='Minimum number of doors')
parser.add_argument('max', type=int, metavar='max_doors', default=5,
					choices=range(3, 10), help='Maximum number of doors')
parser.add_argument('--samples', type=int, metavar='num', default=1000,
					help='Number of iterations to use for sampling, default=1000')

args = parser.parse_args()


try:
	res = subprocess.run('storm -v', shell=True, check=True,
					 capture_output=True, text=True)
except:
	print(f'Failed to find or run Storm executable.')
	exit(1)

MIN_DOORS = args.min
MAX_DOORS = args.max
SAMPLES_NUM = args.samples
print(f'Running demonstration with min={MIN_DOORS}, max={MAX_DOORS}.')


print(f'Starting sampling (n={SAMPLES_NUM})')
for params in monty.param_combs(MIN_DOORS, MAX_DOORS):
	mean, hist, times, sem = sample_params(params, max_run=SAMPLES_NUM)
	data = np.transpose((times, mean, sem))
	# indices = data[gen_indices(SAMPLES_NUM), :]
	fname = '{}/sample_{}d{}p{}o.csv'.format(dir_samples, *params)
	np.savetxt(fname,
			data,
			delimiter=',',
			header='time, mean, sem',
			comments='',
			fmt='%.5f')
	print(f'Finished {fname}')
print(f'Done sampling.')


print(f'Starting translation...')
run_translation(MIN_DOORS, MAX_DOORS, dir_models)
print(f'Output written to {dir_models}')


print('Running Storm...')
subprocess.run(f'bash {CWD}/run_computation.sh', shell=True)
# res = subprocess.run(cmd, shell=True, check=True,
#                      capture_output=True, text=True)

print('Processing output...')

process_files(MIN_DOORS, MAX_DOORS)
print(f'Output written to {CWD}/translation_overview.csv')


