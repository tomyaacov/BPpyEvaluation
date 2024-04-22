import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
import itertools
import numpy as np
from scipy import stats
from time import perf_counter_ns

class EvaluatorListener(bp.PrintBProgramRunnerListener):
    def starting(self, b_program):
        self.events = []
    def ended(self, b_program):
        pass
    def event_selected(self, b_program, event):
        self.events.append(event.name)
        if len(self.events) == 20:
            raise TimeoutError()

def generate_model(doors_num=3, prizes_num=1, doors_opened_num=1,
                   mode=bp.execution_thread):
    if prizes_num + doors_opened_num >= doors_num:
        return "Invalid parameters"
    doors = [x for x in range(doors_num)]
    all_open = [bp.BEvent(f'open{d}') for d in doors]

    @mode
    def hide_prizes():
        prizes = yield choice({i: 1 / len(doors) for i in doors},
                             repeat=prizes_num, replace=False,sorted=True)
        if prizes_num == 1:
            prizes = (prizes,)
        for hide in prizes:
            yield sync(request=bp.BEvent(f'hide{hide}'))
        yield sync(request=bp.BEvent('done_hiding'))
        dont_open = [bp.BEvent(f'open{d}') for d in prizes]
        yield sync(block=dont_open, waitFor=bp.BEvent('done_host_opening'))
        final_door = yield sync(waitFor=all_open)
        if int(final_door.name[4:]) in prizes:
            yield sync(request=bp.BEvent('win'))
        else:
            yield sync(request=bp.BEvent('lose'))

    @mode
    def make_a_guess():
        yield sync(waitFor=bp.BEvent('done_hiding'))
        guess = 0
        yield sync(request=bp.BEvent(f'guess{guess}'))
        yield sync(block=bp.BEvent(f'open{guess}'))

    @mode
    def open_doors():
        yield sync(waitFor=[ bp.BEvent(f'guess{d}') for d in doors])

        blocked = []
        for _ in range(doors_opened_num):
          e = yield sync(request=[e for e in all_open if e not in blocked])
          blocked += [e]

        yield sync(request=bp.BEvent('done_host_opening'))
        yield sync(request=[e for e in all_open if e not in blocked])

    bp_gen = lambda: bp.BProgram(bthreads=[hide_prizes(), make_a_guess(), open_doors()],
                             event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                             listener=EvaluatorListener())
    event_list = ([bp.BEvent('done_hiding'), bp.BEvent('done_host_opening'), bp.BEvent('guess0')] +
                  [bp.BEvent(e) for e in ['win', 'lose']] + 
                  [bp.BEvent(f'{action}{i}') for action, i in itertools.product(['hide', 'open'], doors)])
    return bp_gen, event_list

def q_params(min_doors=3,max_doors=10):
    combs = []
    for d in range(min_doors, max_doors+1):
        for p in range(1, d):
            for o in range(1, d-p):
                combs.append((d,p,o))
    return combs
combs = q_params()

def sample_comb(dpo=(3,1,1), gen_function=generate_model, max_run=1000):
    d,p,o = dpo
    bp_gen, _ = gen_function(d, p, o, mode=bp.execution_thread)
    hist = []
    hist_mean, mean = [], 0
    times = []
    start_time = perf_counter_ns()
    for n in range(1, max_run):
        model = bp_gen()
        model.run()
        res = model.listener.events
        new_val = int('win' in res)
        hist.append(new_val)
        delta = new_val - mean
        mean += delta / n
        hist_mean.append(mean)
        times.append(perf_counter_ns()-start_time)
    return(np.array(hist_mean), hist, np.array(times)/1000000000)

for params in q_params(3, 10):
  mean, hist, times = sample_comb(params, max_run=10000)
  sem = [stats.sem(hist[0:n]) for n in range(0, len(hist))]
  np.savetxt('win_event/sample_{}d{}p{}o.csv'.format(*params), np.transpose((mean,sem,
                times, mean+sem, mean-sem)), delimiter=',',header='mean, sem, time, max_sem, min_sem', comments='')
  print('finished {}d{}p{}o.csv'.format(*params))
