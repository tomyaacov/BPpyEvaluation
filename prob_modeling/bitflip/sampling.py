import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
import warnings
import bit_flip
import numpy as np
from scipy import stats
from time import perf_counter_ns


def comp_sem(hist):
    with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            sem = [stats.sem(hist[0:n]) for n in range(0, len(hist))]
    return sem


similar_bits = lambda s, n: abs(s.count('T') - s.count('F')) < 2

def sample_params(nm=(2,2), max_run=1000, to=3.6e+12):
    n,m = nm
    bp_gen = bit_flip.generate_model(n,m)
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
        if times[-1] > to: #1h
            break
    sem = comp_sem(hist)
    return(np.array(hist_mean), hist, np.array(times) / 1e+9, sem)

if __name__ == '__main__':
    for params in bit_flip.param_combs():
        print('started {}n {}m'.format(*params))
        mean, hist, times, sem = bit_flip.generate_model(params, max_run=10000)
        np.savetxt('samples/sample_{}n{}m.csv'.format(*params), np.transpose((mean,sem,
                        times, mean+sem, mean-sem)), delimiter=',',header='mean, sem, time, max_sem, min_sem', comments='')
        print('finished {}n{}m.csv'.format(*params))
        print(mean[-1], len(hist))
