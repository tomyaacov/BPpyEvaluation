from dfs import DFSBProgram
import argparse
from cinderella import init_bprogram, get_event_list, get_action_list
import pickle
from bppy.model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy
import random
import time
from bppy import BEvent


parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[4, 5, 3, 5])
args = parser.parse_args()


A = int(args.parameters[0])
B = int(args.parameters[1])
C = int(args.parameters[2])
N = int(args.parameters[3])


dfs = DFSBProgram(lambda: init_bprogram(A, B, C, N), get_event_list(B, C, N), max_trace_length=10 ** 10, interrupt_on_trace=False)
time_start = time.time()
init_s, visited = dfs.run()
time_end = time.time()
import bppy
print(bppy.__version__)
print("Time: " + str(time_end - time_start))
print("States: " + str(len(visited)))


# before = 0
# after = 0
# for x in visited:
#     if hasattr(x, "flagged"):
#         after += 1
#     else:
#         x.flagged = False
#     for k, v in x.transitions.items():
#         if not hasattr(v, "flagged"):
#             v.flagged = False
# while before != after:
#     before = after
#     for x in visited:
#         if x.flagged:
#             continue
#         if any([y.flagged for y in x.transitions.values()]):
#             x.flagged = True
#             after += 1

def generate_trace(bprogram_gen):
    trace = []
    ess = SimpleEventSelectionStrategy()
    bprogram = bprogram_gen()
    bprogram.setup()
    while True:
        if len(ess.selectable_events(bprogram.tickets)) == 0:
            return trace, BEvent("AddBlueberries") in trace
        else:
            e = ess.select(bprogram.tickets)
            bprogram.advance_bthreads(bprogram.tickets, e)
        trace.append(e)

# def generate_trace2(init_s, visited, good):
#     current_s = init_s
#     trace = []
#     ess = SimpleEventSelectionStrategy()
#     while True:
#         if len(ess.selectable_events([x.data for x in current_s.nodes if x.data is not None])) == 0:
#             return trace, current_s.flagged
#         if good:
#             e, current_s = random.choice([(k, v) for k, v in current_s.transitions.items() if v.flagged])
#         else:
#             e, current_s = random.choice([(k, v) for k, v in current_s.transitions.items()])
#         current_s = visited[visited.index(current_s)]
#         trace.append(e)


traces = []
for i in range(TESTED_TRACES):
    traces.append(generate_trace(bprogram_gen=lambda: init_bprogram(N, M)))

print(len([x for x in traces if x[1]]))

with open(f'traces_{N}_{M}.pkl', 'wb') as f:
    pickle.dump(traces, f)
