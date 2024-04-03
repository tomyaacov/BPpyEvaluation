import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
import itertools
import numpy as np
from scipy import stats
from time import perf_counter_ns
from math import ceil, log2

class EvaluatorListener(bp.PrintBProgramRunnerListener):
    def starting(self, b_program):
        self.events = []
    def ended(self, b_program):
        pass
    def event_selected(self, b_program, event):
        self.events.append(event.name)
        if len(self.events) >= 200:
            raise TimeoutError()

def generate_model(n=6, mode=bp.execution_thread):
    @mode
    def node(u, x):
        while True:
          yield sync(waitFor=bp.BEvent(f'n{u}_{x}'))
          if u >= n:
            # last layer
            if (x >= n):
              yield sync(request=bp.BEvent(f'n{u-n}_{x%n}'))
            else:
              yield sync(request=bp.BEvent(f'result_{x}'))
          else:
            # inner node
            flip = yield choice({0:0.5, 1:0.5})
            yield sync(request=bp.BEvent(f'n{u*2}_{2*x+flip}'))

    @mode
    def start():
        yield sync(request=bp.BEvent(f'n1_0'))

    d = 1
    nodes = []
    while d > 0 and (d, 0) not in nodes:
        nodes = nodes + [(d*(2**u), x) for u in range(ceil(log2(n/d))+1) for x in range(d*(2**u))]
        d = nodes[-1][0] - n
    #', '.join([str(l) for l in nodes])

    bp_gen = lambda: bp.BProgram(bthreads=[node(*vertex) for vertex in nodes]+[start()],
                             event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                             listener=EvaluatorListener())
    event_list = [bp.BEvent(f'n{u}_{x}') for u, x in nodes] + [bp.BEvent(f'result_{x}') for x in range(n)]
    return bp_gen, event_list


def sample_comb(dice_n=6, gen_function=generate_model, max_run=1000):
    bp_gen, _ = gen_function(dice_n)
    hist = []
    hist_mean, mean = [], 0
    times = []
    start_time = perf_counter_ns()
    for n in range(1, max_run):
        model = bp_gen()
        model.run()
        res = model.listener.events
        new_val = int(f'result_{dice_n-1}' in res)
        hist.append(new_val)
        delta = new_val - mean
        mean += delta / n
        hist_mean.append(mean)
        times.append(perf_counter_ns()-start_time)
    return(np.array(hist_mean), hist, np.array(times)/1000000000)


for dice_n in range(6, 8):
  mean, hist, times = sample_comb(dice_n, max_run=10000)
  sem = [stats.sem(hist[0:n]) for n in range(0, len(hist))]
  np.savetxt('dice/sampling/dice_{}.csv'.format(dice_n), np.transpose((mean,sem,
                times, mean+sem, mean-sem)), delimiter=',',header='mean, sem, time, max_sem, min_sem', comments='')
  print('finished {}.csv'.format(dice_n))
