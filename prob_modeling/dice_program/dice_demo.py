import argparse
import subprocess
import bppy as bp
from bppy.analysis.bprogram_converter import BProgramConverter
import dice
import numpy as np
from time import perf_counter_ns
from dice.read_log import extract_data_re


parser = argparse.ArgumentParser(
	description='BPpy dice problem solving demonstation. Runs sampling and translation + model checking of a problem with the given parameter.')
parser.add_argument('sides', type=int, metavar='sides', default=6,
					choices=range(4, 50), help='Number of sides in the simulated dice.')
parser.add_argument('--samples', type=int, metavar='samples', default=1000,
					help='Number of iterations to use for sampling, default=1000')

args = parser.parse_args()

try:
	res = subprocess.run(PRISM_EXECUTABLE_LOCATION, shell=True, check=True,
					 capture_output=True, text=True)
except:
	print(f'Failed to find or run PRISM executable at {PRISM_EXECUTABLE_LOCATION}')
	print(f'Change path constant PRISM_EXECUTABLE_LOCATION or check requirements.')
	exit(1)

dice_sides = args.sides
SAMPLES_NUM = args.samples
print(f'Running demonstration with n={dice_sides}.')

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

print(f'Starting sampling (n={SAMPLES_NUM})')
mean, _, times =  sample_comb(dice_sides, max_run=SAMPLES_NUM)
print(f'Done')
print(f'Time taken was {times[-1]}s, avg {np.mean(times)/SAMPLES_NUM}s per iteration.')
print(f'Approximated result = {mean[-1]}')


bp_gen, event_list = generate_model(n=dice_sides,
									mode=bp.analysis_thread)
event_nums = {e.name: i for i, e in enumerate(event_list)}
print('Starting model translation...')

start = perf_counter()
conv = BProgramConverter(bp_gen, event_list)
output = conv.to_prism('dice.pm')
end = perf_counter()-start
print(f'Finished translation. Time taken = {end}s.')
print('Output written to dice.pm')

prob_n = f'(F event=' + str(event_nums[event_list[-1].name]) + ')'
with open("prop_dice.csl", 'w+') as f:
	f.write(f"P=? [{prob_n}]")
print(f'Property written to prop.csl')

print('Running PRISM (instead of STORM for portability reasons)')

cmd = PRISM_EXECUTABLE_LOCATION + ' -dtmc dice.pm prop_dice.csl'
res = subprocess.run(cmd, shell=True, check=True,
                     capture_output=True, text=True)

print('Done')
text = res.stdout
rgx_res = r'Result: ([\d|.]+)\S.'
rgx_time = r'Time for model checking: ([\d.]+) seconds.'

prism_res = re.findall(rgx_res, text)[0]
prism_time = re.findall(rgx_time, text)[0]

print(f'Time taken was {prism_time}s.')
print(f'Result =  {prism_res}')
