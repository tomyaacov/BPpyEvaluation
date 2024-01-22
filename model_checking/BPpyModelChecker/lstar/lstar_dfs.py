import pynusmv
pynusmv.init.init_nusmv()
from bp_modules import *


def run(bt_list, event_list, dot_file_name):
    main = main_module(event_list, bt_list)
    # print(bt_list[0])
    # print(bt_list[1])
    # print(main)
    pynusmv.glob.load(*bt_list, main)
    pynusmv.glob.compute_model()
    fsm = pynusmv.glob.prop_database().master.bddFsm

    def get_id(state):
        return {k: v for k, v in state.get_str_values().items() if "state" in k }

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
        _states = {str(v[0]): k for k, v in states.items()}
        g = graphviz.Digraph()
        for s in states:
            g.node(str(s), shape='doublecircle', label=str(s))
        g.node("__start0", shape='none', label="")
        for s, v in states.items():
            for e, s_new in v[1].items():
                if e == "DONE":  # maybe unnecssary
                    continue
                g.edge(str(s), str(_states[str(s_new)]), label=e)
        g.edge("__start0", "0", label="")
        g.save(name)
        return g

    save_graph(l, dot_file_name)
