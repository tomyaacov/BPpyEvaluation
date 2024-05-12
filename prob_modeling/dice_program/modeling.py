import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
from bppy.analysis.bprogram_converter import BProgramConverter
from time import perf_counter_ns
import dice

def run_translation(min_d, max_d, FILEDIR = 'models'):
    for dice_n in range(min_d, max_d):
        bp_gen, event_list = dice.generate_model(n=dice_n,
                                            mode=bp.analysis_thread)
        event_nums = {e.name: i for i, e in enumerate(event_list)}
        conv = BProgramConverter(bp_gen, event_list)
        start = perf_counter_ns()
        conv.to_prism('{}/dice_{}.pm'.format(FILEDIR, dice_n))

        time_taken = (perf_counter_ns() - start) / 1e+9
        with open(f'{FILEDIR}/time_taken.txt', 'a') as f:
            f.write(f'time for {dice_n}: {time_taken}\n')

        prob_n = f'(F event=' + str(event_nums[event_list[-1].name]) + ')'
        with open("{}/prop_{}.csl".format(FILEDIR, dice_n), 'w+') as f:
            f.write(f"P=? [{prob_n}]")
        print("finished ({}) in {}s.".format(dice_n, time_taken))
        
if __name__ == '__main__':
    run_translation(6, 10)