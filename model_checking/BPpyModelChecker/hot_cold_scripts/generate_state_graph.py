import pynusmv
pynusmv.init.init_nusmv()
# pynusmv.glob.load_from_file("hot_cold2.smv")
from bp_modules import *
from examples.hot_cold import *
event_list = ["Start", "HOT", "COLD0"]
# N = 3
# M = 1
# set_bprogram(N, M)
# bt_list = [
#     bthread_to_module(lambda: add_a(), "adda", event_list),
#     bthread_to_module(lambda: add_b("COLD0"), "addb", event_list),
#     bthread_to_module(lambda: control(), "control", event_list),
# ]
# main = main_module(event_list, bt_list)
# print(bt_list[0])
# print(bt_list[1])
# print(bt_list[2])
# print(main)

# with open("output/bp_model_new.smv", "w") as f:
#     for bt in bt_list:
#         f.write(str(bt))
#         f.write("\n")
#     f.write(str(main))
#     f.write("\n")
pynusmv.glob.load_from_file("/Users/tomyaacov/repos/BPpyModelChecker/output/bp_model.smv")

pynusmv.glob.compute_model()


# pynusmv.glob.load(bt_list[0], bt_list[1], bt_list[2], main)
# pynusmv.glob.compute_model()
fsm = pynusmv.glob.prop_database().master.bddFsm

def get_id(state):
    return {k:v for k,v in state.get_str_values().items() if k.endswith("state") or k.endswith("must_finish") or k.endswith("DEADLOCK")}

l = {}
def dfs(s):
    if get_id(fsm.pick_one_state(s)) in [x for x, _ in l.values()]:
        return
    k = len(l)
    l[k] = (get_id(fsm.pick_one_state(s)), {})
    for next in fsm.pick_all_states(fsm.post(s)):
        l[k][1][next.get_str_values()["event"]] = get_id(next)
        dfs(next)
dfs(fsm.init)
print(len(l))



import graphviz
def save_graph(states, name):
    _states = {str(v[0]): k for k,v in states.items()}
    g = graphviz.Digraph()
    for s in states:
        g.node(str(s), shape='doublecircle' if s == 0 else 'circle', color="red" if states[s][0].get('DEADLOCK', "FALSE") == "TRUE" else "green")
    for s, v in states.items():
        for e, s_new in v[1].items():
            g.edge(str(s), str(_states[str(s_new)]), label=e)
    g.save(name)
    return g
save_graph(l, "output/bp_state_graph.dot")