from bppy.utils.dfs import DFSBProgram
from pancake import init_bprogram, get_event_list
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--n", default=10)
parser.add_argument("--m", default=1)

args = parser.parse_args()

N = int(args.n)
M = int(args.m)

dfs = DFSBProgram(lambda: init_bprogram(N, M), get_event_list(N), max_trace_length=10**10)

init_s, visited = dfs.run()
print("N:", N, "M:", M)
print("number of events:", len(get_event_list(N)))
print("number of states:", len(visited))