import argparse, os, shutil, subprocess
import numpy as np
import math
import dice

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
	description='BPpy dice problem solving demonstation. Runs sampling and translation + model checking of a given parameter range.')
parser.add_argument('min', type=int, metavar='min_sides', default=6,
					choices=range(6, 50), help='Minimal number of sides in the simulated dice.')
parser.add_argument('max', type=int, metavar='max_sides', default=35,
					choices=range(6, 50), help='Maximal number of sides.')
parser.add_argument('--samples', type=int, metavar='samples', default=1000,
					help='Number of iterations to use for sampling, default=1000')

args = parser.parse_args()


try:
	res = subprocess.run('storm -v', shell=True, check=True,
					 capture_output=True, text=True)
except:
	print(f'Failed to find or run Storm executable.')
	exit(1)

MIN_SIDES = args.min
MAX_SIDES = args.max +1 # range is end exclusive
SAMPLES_NUM = args.samples
print(f'Running demonstration with min={MIN_SIDES}, max={MAX_SIDES -1}.')

print(f'Starting sampling (n={SAMPLES_NUM})')
for params in range(MIN_SIDES, MAX_SIDES):
	mean, hist, times, sem = sample_params(params, max_run=SAMPLES_NUM)
	data = np.transpose((times, mean, sem))
	# indices = data[gen_indices(SAMPLES_NUM), :]
	fname = '{}/sample_{}n.csv'.format(dir_samples, params)
	np.savetxt(fname,
			data,
			delimiter=',',
			header='time, mean, sem',
			comments='',
			fmt='%.5f')
	print(f'Finished {fname}')
print(f'Done sampling.')


print(f'Starting translation...')
run_translation(MIN_SIDES, MAX_SIDES, dir_models)
print(f'Output written to {dir_models}')



print('Running Storm...')
subprocess.run(f'bash {CWD}/run_computation.sh', shell=True)
# res = subprocess.run(cmd, shell=True, check=True,
#                      capture_output=True, text=True)

print('Processing output...')

process_files(MIN_SIDES, MAX_SIDES)
print(f'Output written to {CWD}/translation_overview.csv')
