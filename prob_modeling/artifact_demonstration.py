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

PRISM_EXECUTABLE_LOCATION = './prism-4.8-linux64-x86/bin/prism'


parser = argparse.ArgumentParser(
	description='BPpy Monty Hall problem solving demonstation. Runs sampling and translation + model checking of a problem with the given parameters.')
parser.add_argument('doors', type=int, metavar='doors', default=3,
					choices=range(3, 10), help='Number of doors in total')
parser.add_argument('prizes', type=int, metavar='prizes', default=1,
					choices=range(1, 9), help='Doors containing prizes')
parser.add_argument('doors_opened', type=int, metavar='opened', default=1,
					choices=range(1, 5), help='Doors opened before asking to swap')
parser.add_argument('--samples', type=int, metavar='num', default=1000,
					help='Number of iterations to use for sampling, default=1000')

args = parser.parse_args()

if args.prizes + args.doors_opened >= args.doors:
	print('Invalid params: number of prizes plus doors opened must be smaller than total doors.')
	exit(1)

try:
	res = subprocess.run(PRISM_EXECUTABLE_LOCATION, shell=True, check=True,
					 capture_output=True, text=True)
except:
	print(f'Failed to find or run PRISM executable at {PRISM_EXECUTABLE_LOCATION}')
	print(f'Change path constant PRISM_EXECUTABLE_LOCATION or check requirements.')

DOORS_NUM = args.doors
PRIZES_NUM = args.prizes
DOORS_OPEN_NUM = args.doors_opened
SAMPLES_NUM = args.samples
print(f'Running demonstration with d={DOORS_NUM}, p={PRIZES_NUM}, o={DOORS_OPEN_NUM}')

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

print(f'Starting sampling (n={SAMPLES_NUM})')
mean, _, times =  sample_comb((DOORS_NUM, PRIZES_NUM, DOORS_OPEN_NUM), max_run=SAMPLES_NUM)
print(f'Done')
print(f'Time taken was {times[-1]}s, avg {np.mean(times)/SAMPLES_NUM}s per iteration.')
print(f'Approximated result = {mean[-1]}')


bp_gen, event_list = generate_model(doors_num=DOORS_NUM,
									prizes_num=PRIZES_NUM,
									doors_opened_num=DOORS_OPEN_NUM,
									mode=bp.analysis_thread)
event_nums = {e.name: i for i, e in enumerate(event_list)}
print('Starting model translation...')
conv = BProgramConverter(bp_gen, event_list)
output = conv.to_prism('monty.prism')
print('Output written to monty.prism')
print('Running PRISM (more portable than Storm)')

cmd = PRISM_EXECUTABLE_LOCATION + ' -dtmc monty.prism -pf "P=? [(F event=3)]"'
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
