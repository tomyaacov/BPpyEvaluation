import argparse
from bppy.utils.dfs import DFSBProgram

parser = argparse.ArgumentParser()

parser.add_argument("--n", default=3)
parser.add_argument("--k", default=1)
parser.add_argument("--m", default=1)

args = parser.parse_args()

from hot_cold import init_bprogram, params, get_event_list

params["n"] = int(args.n)
params["k"] = int(args.k)
params["m"] = int(args.m)
name = "_".join([str(key) + "_" + str(value) for key, value in vars(args).items()])

dfs = DFSBProgram(init_bprogram, get_event_list(), max_trace_length=10**10)
init_s, visited = dfs.run()
print("number of states:", len(visited))