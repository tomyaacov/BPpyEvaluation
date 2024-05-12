import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
import warnings
import dice
import numpy as np
from scipy import stats
from time import perf_counter_ns

def comp_sem(hist):
    with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            sem = [stats.sem(hist[0:n]) for n in range(0, len(hist))]
    return sem

def sample_params(dice_n=6, gen_function=dice.generate_model, max_run=1000):
    bp_gen, _ = gen_function(dice_n)
    hist = []
    hist_mean, mean = [], 0
    times = []
    start_time = perf_counter_ns()
    for n in range(1, max_run):
        model = bp_gen()
        model.run()
        res = model.listener.events
        new_val = int(f'result_{dice_n-1}' in res[-1])
        hist.append(new_val)
        delta = new_val - mean
        mean += delta / n
        hist_mean.append(mean)
        times.append(perf_counter_ns()-start_time)
    sem = comp_sem(hist)
    return (np.array(hist_mean), hist, np.array(times) / 1e+9, sem)

if __name__ == '__main__':
    for dice_n in range(6, 31):
        mean, hist, times, sem = sample_params(dice_n, max_run=10000)
        np.savetxt('sampling/dice_{}.csv'.format(dice_n), np.transpose((mean,sem,
                        times, mean+sem, mean-sem)), delimiter=',',header='mean, sem, time, max_sem, min_sem', comments='')
        print('finished {}.csv'.format(dice_n))
