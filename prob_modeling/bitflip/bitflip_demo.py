import argparse
import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
from bppy.analysis.bprogram_converter import BProgramConverter
import itertools
import numpy as np
from time import perf_counter_ns
import subprocess
import re
from bit_flip_exe import bit_flip_bp


parser = argparse.ArgumentParser(
	description='BPpy bitflip demonstation. Runs only sampling a problem with the given parameters.')
parser.add_argument('N', type=int, metavar='n', default=2,
					choices=range(2, 5), help='Number of rows in the matrix.')
parser.add_argument('M', type=int, metavar='m', default=2,
					choices=range(2, 5), help='Number of columns in the matrix')
parser.add_argument('--samples', type=int, metavar='num', default=1000,
					help='Number of iterations to use for sampling, default=1000')

args = parser.parse_args()


N_NUM = args.N
M_NUM = args.M
SAMPLES_NUM = args.samples
print(f'Running demonstration with N={N_NUM}, M={M_NUM}')


similar_bits = lambda s: abs(s.count('T') - s.count('F')) < 2

def sample_comb(nm=(2,2), max_run=1000):
    n,m = nm
    bp_gen = bit_flip_bp(n,m)
    hist = []
    hist_mean, mean = [], 0
    times = []
    start_time = perf_counter_ns()
    for n in range(1, max_run):
        model = bp_gen()
        model.run()
        res = model.listener.events
        new_val =  int(similar_bits(res[-1]))  # 1 if true, 0 false
        hist.append(new_val)
        delta = new_val - mean
        mean += delta / n
        hist_mean.append(mean)
        times.append(perf_counter_ns()-start_time)
        if times[-1] > 3.6e+12:
            break
    return(np.array(hist_mean), hist, np.array(times)/1000000000)

print(f'Starting sampling (N={SAMPLES_NUM})')
mean, _, times =  sample_comb((N_NUM, M_NUM), max_run=SAMPLES_NUM)
print(f'Done')
print(f'Time taken was {times[-1]}s, avg {np.mean(times)/SAMPLES_NUM}s per iteration.')
print(f'Approximated result = {mean[-1]}')
