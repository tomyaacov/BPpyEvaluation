from bppy.utils.dfs import DFSBProgram
# from pancake import init_bprogram, get_event_list
from pancake import init_bprogram, get_event_list
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument("--n", default=3)
parser.add_argument("--m", default=1)

args = parser.parse_args()

N = int(args.n)
M = int(args.m)

dfs = DFSBProgram(lambda: init_bprogram(N, M), get_event_list(), max_trace_length=10**10)


start = time.time()
init_s, visited = dfs.run()
end = time.time()
print("------------------------------------")
print("N:", N, "M:", M)
print("TIME:", end - start)
print("number of events:", len(get_event_list()))
print("number of states:", len(visited))


