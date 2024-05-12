import argparse, os, shutil, subprocess
import numpy as np
import bit_flip

from sampling import sample_params

# cleans existing directories
CWD = os.path.dirname(os.path.realpath(__file__))
dir_samples = CWD + '/samples'
if os.path.exists(dir_samples):
    shutil.rmtree(dir_samples)
os.makedirs(dir_samples)


parser = argparse.ArgumentParser(
	description='BPpy bitflip demonstation. Runs only sampling a problem with the given parameters.')
parser.add_argument('N', type=int, metavar='n', default=2,
					choices=range(2, 5), help='Number of rows in the matrix.')
parser.add_argument('M', type=int, metavar='m', default=2,
					choices=range(2, 10), help='Number of columns in the matrix')
parser.add_argument('--samples', type=int, metavar='samples', default=1000,
					help='Number of iterations to use for sampling, default=1000')
parser.add_argument('-q', '--quiet',
                    action='store_true')
args = parser.parse_args()

N_NUM = args.N
M_NUM = args.M
SAMPLES_NUM = args.samples
quiet = args.quiet

if not quiet:
    print(f'Running demonstration with N={N_NUM}, M={M_NUM}, samples={SAMPLES_NUM}')

mean, hist, times, sem = sample_params((N_NUM, M_NUM),
                                       max_run=SAMPLES_NUM,
                                       to=360*1e+9)
avg_time =  times[-1] / len(mean)
if not quiet:
    print(f'Finished {len(mean)} samples in {times[-1]}s (average {avg_time}).')
    print(f'Final mean: {mean[-1]}')
    print(f'Final SEM: {sem[-1]}')
else:
    print(f'{N_NUM}x{M_NUM}, {mean[-1]:.5f}, {sem[-1]:.5f}, {len(mean)}, {avg_time:.5f}')