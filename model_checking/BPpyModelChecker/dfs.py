import graphviz
from bppy import BEvent, SimpleEventSelectionStrategy
from itertools import product

class Node:
    def __init__(self, prefix, data):
        self.prefix = prefix
        self.data = data
        self.transitions = {}
        if data is None:
            self.must_finish = False
        else:
            self.must_finish = data.get('must_finish', False)

    def __key(self):
        return str(self.data)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __str__(self):
        return str(self.prefix) + str(self.data)


class DFSBThread:
    def __init__(self, bthread_gen, ess, event_list):
        self.bthread_gen = bthread_gen
        self.ess = ess
        self.event_list = event_list

    def get_state(self, prefix):
        bt = self.bthread_gen()
        s = bt.send(None)
        for e in prefix:
            if s is None:
                break
            if 'block' in s:
                if isinstance(s.get('block'), BEvent):
                    if BEvent(e) == s.get('block'):
                        return None
                else:
                    if BEvent(e) in s.get('block'):
                        return None
            if self.ess.is_satisfied(BEvent(e), s):
                s = bt.send(BEvent(e))
        if s is None:
            return {}
        return {k: DFSBThread.str_event(v) if k in ["request", "waitFor", "block"] else v for k, v in s.items() }

    def compute_event_list(self):
        pass

    def run(self):
        init_s = Node(tuple(), self.get_state(tuple()))
        visited = set()
        requested = set()
        blocked = set()
        stack = []
        stack.append(init_s)

        while len(stack):
            s = stack.pop()
            if s not in visited:
                visited.add(s)
            if "request" in s.data:
                requested.update(s.data["request"])
            if "block" in s.data:
                blocked.update(s.data["block"])

            for e in self.event_list:
                new_s = Node(s.prefix + (e,), self.get_state(s.prefix + (e,)))
                if new_s.data is None:
                    continue
                s.transitions[e] = new_s
                if new_s not in visited:
                    stack.append(new_s)
        return init_s, visited, requested, blocked

    @staticmethod
    def save_graph(init, states, name):
        g = graphviz.Digraph()
        map = {}
        for i, s in enumerate(states):
            g.node(str(i), shape='doublecircle' if s == init else 'circle')
            map[s] = str(i)
        for s in states:
            for e, s_new in s.transitions.items():
                g.edge(map[s], map[s_new], label=e)
        g.save(name)
        return g

    @staticmethod
    def str_event(e):
        if isinstance(e, BEvent):
            return {e.name}
        elif isinstance(e, str):
            return {e}
        return set([ee.name for ee in e])

class ProductNode:
    def __init__(self, l):
        self.l = l
        self.transitions = {}

    def __key(self):
        return "_".join([str(x.data) for x in self.l])

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

class DFSBProgram:
    def __init__(self, bthread_gens, ess, event_list):
        self.bthread_gens = bthread_gens
        self.ess = ess
        self.event_list = event_list

    def run(self):
        bt_dfs = {}
        for i in range(len(self.bthread_gens)):
            dfs = DFSBThread(self.bthread_gens[i], self.ess, self.event_list)
            bt_dfs[i] = dfs.run()
            DFSBThread.save_graph(*bt_dfs[i][:2], f"output/dfs{i}.dot")

        init_s = ProductNode(tuple([v[0] for _, v in bt_dfs.items()]))
        visited = set()
        stack = []
        stack.append(init_s)

        while len(stack):
            s = stack.pop()
            if s not in visited:
                visited.add(s)

            for e in set().union(*[si.data.get("request", {}) for si in s.l]):
                new_s = ProductNode(tuple([si.transitions.get(e, None) for si in s.l]))
                if any([x is None for x in new_s.l]):
                    continue
                new_s = ProductNode(tuple([[x for x in bt_dfs[i][1] if x == new_s.l[i]][0] for i in range(len(new_s.l))]))
                s.transitions[e] = new_s
                if new_s not in visited:
                    stack.append(new_s)
        return init_s, visited

    @staticmethod
    def save_graph(init, states, name):
        g = graphviz.Digraph()
        map = {}
        for i, s in enumerate(states):
            g.node(str(i), shape='doublecircle' if s == init else 'circle')
            map[s] = str(i)
        for s in states:
            for e, s_new in s.transitions.items():
                g.edge(map[s], map[s_new], label=e)
        g.save(name)
        return g


if __name__ == "__main__":
    # from examples.dining_philosophers import *
    # N = 3
    # set_dp_bprogram(3)
    # all_events = [BEvent(f"T{i}R") for i in range(N)] + \
    #              [BEvent(f"T{i}L") for i in range(N)] + \
    #              [BEvent(f"P{i}R") for i in range(N)] + \
    #              [BEvent(f"P{i}L") for i in range(N)] + \
    #              [BEvent(f"TS{i}") for i in range(N)] + \
    #              [BEvent(f"RS{i}") for i in range(N)]
    # dfs = DFSBProgram(list(map((lambda n: lambda: philosopher(n)), range(N))) +
    #                   list(map((lambda n: lambda: fork(n)), range(N))) +
    #                   [lambda: fork_eventually_released(0)], #+
    #                   # [lambda: semaphore()] +
    #                   # list(map((lambda n: lambda: take_semaphore(n)), range(N))),
    #                   SimpleEventSelectionStrategy(),
    #                   [x.name for x in all_events])
    # init_s, visited = dfs.run()
    # DFSBProgram.save_graph(init_s, visited, "output/dfs.dot")
    from examples.hot_cold import *
    N = 3
    M = 1
    set_bprogram(N, M)
    event_list = ["HOT"] + ["COLD" + str(i) for i in range(M)]
    dfs = DFSBProgram([lambda: add_a(), lambda: add_b("COLD0"), lambda: control()],
                      SimpleEventSelectionStrategy(),
                      event_list)
    init_s, visited = dfs.run()
    DFSBProgram.save_graph(init_s, visited, "output/dfs.dot")
    # from examples.ttt import *
    # R=2
    # C=2
    # set_ttt_bprogram(R, C)
    # any_x = [x(i, j) for i in range(R) for j in range(C)]
    # any_o = [o(i, j) for i in range(R) for j in range(C)]
    # move_events = any_x + any_o
    # all_events = move_events + [BEvent('OWin'), BEvent('XWin'), BEvent('Draw')]
    # LINES = [[(i, j) for j in range(C)] for i in range(R)] + [[(i, j) for i in range(R)] for j in range(C)] + [
    #     [(i, i) for i in range(R)]] + [[(i, R - i - 1) for i in range(R)]]
    # x_lines = [[x(i, j) for (i, j) in line] for line in LINES]
    # o_lines = [[o(i, j) for (i, j) in line] for line in LINES]
    # dfs = DFSBProgram(list(map((lambda arg: lambda: square_taken(*arg)), product(range(R), range(C)))) +
    #                       [lambda: enforce_turns(), lambda: end_of_game(), lambda: detect_draw(), lambda: player_o(), lambda: player_x()] +
    #                       list(map((lambda line: lambda: detect_x_win(line)), x_lines)) +
    #                       list(map((lambda line: lambda: detect_x_win(line)), o_lines)),
    #                   SimpleEventSelectionStrategy(),
    #                   [x.name for x in all_events])
    # init_s, visited = dfs.run()
    # DFSBProgram.save_graph(init_s, visited, "output/dfs.dot")


