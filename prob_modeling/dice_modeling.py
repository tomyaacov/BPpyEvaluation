import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
from bppy.analysis.bprogram_converter import BProgramConverter
import itertools
import numpy as np
from scipy import stats
from time import perf_counter, perf_counter_ns
from math import ceil, log2

class EvaluatorListener(bp.PrintBProgramRunnerListener):
    def starting(self, b_program):
        self.events = []
    def ended(self, b_program):
        pass
    def event_selected(self, b_program, event):
        self.events.append(event.name)
        if len(self.events) == 20:
            raise TimeoutError()

def generate_model(n =6, mode=bp.execution_thread):

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


for dice_n in range(6, 20):
    bp_gen, event_list = generate_model(n=dice_n,
                                        mode=bp.analysis_thread)
    event_nums = {e.name: i for i, e in enumerate(event_list)}
    conv = BProgramConverter(bp_gen, event_list)
    start = perf_counter()
    output = conv.to_prism('dice/models/dice_{}.pm'.format(dice_n))

    end = perf_counter()-start
    with open('dice/models/time_taken.txt', 'a') as f:
        f.write(f'time for {dice_n}: {end}\n')

    prob_n = f'(F event=' + str(event_nums[event_list[-1].name]) + ')'
    with open("dice/models/prop_{}.csl".format(dice_n), 'w+') as f:
        f.write(f"P=? [{prob_n}]")
    print("finished {}".format(dice_n))