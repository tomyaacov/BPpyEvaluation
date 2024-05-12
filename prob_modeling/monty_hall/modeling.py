import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
from bppy.analysis.bprogram_converter import BProgramConverter
from time import perf_counter_ns
import monty


def run_translation(min_d, max_d, FILEDIR = 'models'):
    for params in monty.param_combs(min_d, max_d):
        d, p, o = params
        bp_gen, event_list = monty.generate_model(doors_num=d,
                                                prizes_num=p,
                                                doors_opened_num=o,
                                                mode=bp.analysis_thread)
        event_nums = {e.name: i for i, e in enumerate(event_list)}
        conv = BProgramConverter(bp_gen, event_list)
        start = perf_counter_ns()
        conv.to_prism('{}/model_{}d{}p{}o.pm'.format(FILEDIR, d, p, o))

        time_taken = (perf_counter_ns() - start) / 1e+9
        with open(f'{FILEDIR}/time_taken.txt', 'a') as f:
            f.write(f'time for {params}: {time_taken}\n')

        win = f'(F event=' + str(event_nums['win']) + ')'
        with open("{}/prop_{}d{}p{}o.csl".format(FILEDIR, *params), 'w+') as f:
            f.write(f"P=? [{win}]")
        print("finished {} in {}s.".format(params, time_taken))

if __name__ == '__main__':
    run_translation(3, 4)