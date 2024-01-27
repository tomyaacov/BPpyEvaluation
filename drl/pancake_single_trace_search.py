from dfs import DFSBProgram, Interrupt
# from pancake import init_bprogram, get_event_list
from pancake import init_bprogram, get_event_list
import argparse
import random


parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[3, 1])
args = parser.parse_args()

N = int(args.parameters[0])
M = int(args.parameters[1])

l = [x for x in range(len(init_bprogram(N, M).bthreads))]
random.shuffle(l)

def bprogram_generator(l):
    a = init_bprogram(N, M)
    a.bthreads = [a.bthreads[x] for x in l]
    return a

event_list = get_event_list()
random.shuffle(event_list)

dfs = DFSBProgram(lambda: bprogram_generator(l), get_event_list(), max_trace_length=10**10)
try:
    init_s, visited = dfs.run()
except Interrupt as e:
    print("Trace found!")
    #print(e.prefix)
    print("trace length:", len(e.prefix))
    exit(0)
print("No trace found!")