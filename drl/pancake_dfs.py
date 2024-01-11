from dfs import DFSBProgram
import argparse
from pancake import init_bprogram, get_event_list, get_action_list
import pickle
from bppy.model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy
import random


parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[3, 1, 10])
args = parser.parse_args()

N = int(args.parameters[0])
M = int(args.parameters[1])
TESTED_TRACES = int(args.parameters[2])

dfs = DFSBProgram(lambda: init_bprogram(N, M), get_event_list(), max_trace_length=10 ** 10, interrupt_on_trace=False)
init_s, visited = dfs.run()

before = 0
after = 0
for x in visited:
    if hasattr(x, "flagged"):
        after += 1
    else:
        x.flagged = False
    for k, v in x.transitions.items():
        if not hasattr(v, "flagged"):
            v.flagged = False
while before != after:
    before = after
    for x in visited:
        if x.flagged:
            continue
        if any([y.flagged for y in x.transitions.values()]):
            x.flagged = True
            after += 1

def generate_trace(init_s, visited, good):
    current_s = init_s
    trace = []
    ess = SimpleEventSelectionStrategy()
    while True:
        if len(ess.selectable_events([x.data for x in current_s.nodes if x.data is not None])) == 0:
            return trace, current_s.flagged
        if good:
            e, current_s = random.choice([(k, v) for k, v in current_s.transitions.items() if v.flagged])
        else:
            e, current_s = random.choice([(k, v) for k, v in current_s.transitions.items()])
        current_s = visited[visited.index(current_s)]
        trace.append(e)


traces = []
for i in range(TESTED_TRACES):
    traces.append(generate_trace(init_s=init_s, visited=visited, good=i % 2 == 0))


with open('traces.pkl', 'wb') as f:
    pickle.dump(traces, f)
