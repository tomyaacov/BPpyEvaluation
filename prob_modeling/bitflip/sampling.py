import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
import itertools
import numpy as np
from scipy import stats
from time import perf_counter_ns
from bit_flip_exe import bit_flip_bp


similar_bits = lambda s, n: abs(s.count('T') - s.count('F')) < 2

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
        new_val =  int(similar_bits(res[-1], n))  # 1 if true, 0 false
        hist.append(new_val)
        delta = new_val - mean
        mean += delta / n
        hist_mean.append(mean)
        times.append(perf_counter_ns()-start_time)
        if times[-1] > 3.6e+12:
            break
    return(np.array(hist_mean), hist, np.array(times)/1000000000)


upper_bound_n = 3
upper_bound_m = 7
combs = itertools.product(range(3,upper_bound_n+1), range(5,upper_bound_m+1))
combs = [(n, m) for n, m in combs if n <= m]

for params in combs:
  print('started {}n {}m'.format(*params))
  mean, hist, times = sample_comb(params, max_run=10000)
  sem = [stats.sem(hist[0:n]) for n in range(0, len(hist))]
  np.savetxt('samples/sample_{}n{}m.csv'.format(*params), np.transpose((mean,sem,
                times, mean+sem, mean-sem)), delimiter=',',header='mean, sem, time, max_sem, min_sem', comments='')
  print('finished {}n{}m.csv'.format(*params))
  print(mean[-1], len(hist))
