from dfs import DFSBProgram
import argparse
from cinderella import init_bprogram, get_event_list, get_action_list
import pickle
from bppy.model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy
import random
import time
from bppy import BEvent


parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[5, 10, 3, 5, 1000])
args = parser.parse_args()


A = int(args.parameters[0])
B = int(args.parameters[1])
C = int(args.parameters[2])
N = int(args.parameters[3])
TESTED_TRACES = int(args.parameters[4])


dfs = DFSBProgram(lambda: init_bprogram(A, B, C, N), max_trace_length=10 ** 10, interrupt_on_trace=False)
time_start = time.time()
init_s, visited = dfs.run()
time_end = time.time()

print("Time: " + str(time_end - time_start))
print("States: " + str(len(visited)))

flags_map = {}
visited_map = {}
for x in visited:
    flags_map[hash(x)] = False
    visited_map[hash(x)] = x

before = 0
after = 0
for x in visited:
    if BEvent("CinderellaWins") in x.transitions:
        after += 1
        flags_map[hash(x)] = True
        flags_map[hash(x.transitions[BEvent("CinderellaWins")])] = True
while before != after:
    before = after
    for x in visited:
        if flags_map[hash(x)]:
            continue
        if any([flags_map[hash(y)] for y in x.transitions.values()]):
            flags_map[hash(x)] = True
            after += 1

def generate_trace(bprogram_gen):
    trace = []
    ess = SimpleEventSelectionStrategy()
    bprogram = bprogram_gen()
    bprogram.setup()
    while True:
        if len(ess.selectable_events(bprogram.tickets)) == 0:
            return trace, BEvent("CinderellaWins") in trace
        else:
            e = ess.select(bprogram.tickets)
            bprogram.advance_bthreads(bprogram.tickets, e)
        trace.append(e)

def generate_trace2(init_s, visited, flags_map, good):
    current_s = init_s
    trace = []
    ess = SimpleEventSelectionStrategy()
    while True:
        if len(ess.selectable_events([x.data for x in current_s.nodes if x.data is not None])) == 0:
            return trace
        if good:
            e, current_s = random.choice([(k, v) for k, v in current_s.transitions.items() if flags_map[hash(v)]])
        else:
            e, current_s = random.choice([(k, v) for k, v in current_s.transitions.items()])
        current_s = visited_map[hash(current_s)]
        trace.append(e)


traces = []
for i in range(TESTED_TRACES//2):
    traces.append((generate_trace2(init_s, visited, flags_map, True), True))
    traces.append(generate_trace(bprogram_gen=lambda: init_bprogram(A, B, C, N)))

print(len([x for x in traces if x[1]]))

with open(f'traces_{A}_{B}_{C}_{N}.pkl', 'wb') as f:
    pickle.dump(traces, f)
