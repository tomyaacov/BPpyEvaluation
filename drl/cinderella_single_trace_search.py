from dfs import DFSBProgram, Interrupt
from cinderella import init_bprogram, get_event_list, get_predicate
import argparse
import random


parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[4, 5, 2, 5]) # N
args = parser.parse_args()


A = int(args.parameters[0])
B = int(args.parameters[1])
C = int(args.parameters[2])
N = int(args.parameters[3])


l = [x for x in range(len(init_bprogram(A, B, C, N).bthreads))]
random.shuffle(l)

def bprogram_generator(l):
    a = init_bprogram(A, B, C, N)
    a.bthreads = [a.bthreads[x] for x in l]
    return a

event_list = get_event_list(B, C, N)
random.shuffle(event_list)


dfs = DFSBProgram(lambda: bprogram_generator(l), get_event_list(B, C, N), max_trace_length=10**10, predicate=get_predicate())
try:
    init_s, visited = dfs.run()
except Interrupt as e:
    print("Trace found!")
    print("trace length:", len(e.prefix))
    exit(0)
print("No trace found!")