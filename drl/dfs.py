from bppy.model.b_event import BEvent
from bppy.model.sync_statement import sync, choice
from bppy.utils.exceptions import BPAssertionError
from bppy.model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy

class Interrupt(Exception):
    def __init__(self, prefix):
        self.prefix = prefix

class Node:
    def __init__(self, prefix, data):
        self.prefix = prefix
        self.data = data
        self.transitions = {}

    def __key(self):
        if isinstance(self.data, choice):
            return str(self.data._id)
        return str(self.data)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __str__(self):
        return str(self.prefix) + str(self.data)

    def __repr__(self):
        return self.__str__()

    def get_key(self):
        return self.__key()


class DFSBThread:
    def __init__(self, bthread_gen, ess, event_list):
        self.bthread_gen = bthread_gen
        self.ess = ess
        self.event_list = event_list

    def get_state(self, prefix):
        bt = self.bthread_gen()
        s = bt.send(None) # s = sync or Choice
        for e in prefix: # e = event or choice key
            if s is None:
                break
            if isinstance(s, sync):
                if 'block' in s:
                    if isinstance(s.get('block'), BEvent):
                        if e == s.get('block'):
                            return None
                    else:
                        if e in s.get('block'):
                            return None
                if self.ess.is_satisfied(e, s):
                    s = bt.send(e)
            elif isinstance(s, choice):
                s = bt.send(e)
        if s is None:
            return sync()
        return s

    def run(self, return_requested_and_blocked=False):
        init_s = Node(tuple(), self.get_state(tuple()))
        visited = set()
        stack = []
        stack.append(init_s)
        requested = set()
        blocked = set()

        while len(stack):
            s = stack.pop()
            if s not in visited:
                visited.add(s)
            if isinstance(s.data, sync) and return_requested_and_blocked:
                if "request" in s.data:
                    if isinstance(s.data["request"], BEvent):
                        requested.add(s.data["request"])
                    else:
                        requested.update(s.data["request"])
                if "block" in s.data:
                    if isinstance(s.data["block"], BEvent):
                        blocked.add(s.data["block"])
                    else:
                        blocked.update([x for x in self.event_list if x in s.data["block"]])
            if isinstance(s.data, choice):
                for c in s.data.keys():
                    new_s = Node(s.prefix + (c,),
                        self.get_state(s.prefix + (c,)))
                    s.transitions[c] = (new_s, s.data[c])
                    if new_s not in visited:
                        stack.append(new_s)
            if isinstance(s.data, sync):
                for e in self.event_list:
                    new_s = Node(s.prefix + (e,), self.get_state(s.prefix + (e,)))
                    if new_s.data is None:
                        continue
                    s.transitions[e] = new_s
                    if new_s not in visited:
                        stack.append(new_s)
        if return_requested_and_blocked:
            return init_s, visited, requested, blocked
        return init_s, visited


class NodeList:
    def __init__(self, nodes, prefix, interrupt_on_trace=True, predicate=None):
        self.nodes = nodes
        self.prefix = prefix
        self.transitions = {}
        ess = SimpleEventSelectionStrategy()
        if len(ess.selectable_events([x.data for x in self.nodes if x.data is not None])) == 0:
            if predicate is not None and predicate(self.prefix):#BEvent("AddBlueberries") in self.prefix:
                if interrupt_on_trace:
                    raise Interrupt(self.prefix)
                else:
                    self.flagged = True

    def __key(self):
        return ";".join([n.get_key() for n in self.nodes])

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()


class DFSBProgram:
    def __init__(self, bprogram_generator, event_list=None, max_trace_length=1000, interrupt_on_trace=True, predicate=None):
        self.bprogram_generator = bprogram_generator
        self.event_list = event_list
        self.max_trace_length = max_trace_length
        self.interrupt_on_trace = interrupt_on_trace
        self.predicate = predicate

    def run(self, explore_graph=True):
        if self.event_list:
            mapper = {}
            init = []
            n = len(self.bprogram_generator().bthreads)
            ess = self.bprogram_generator().event_selection_strategy
            for i in range(n):
                f = lambda: self.bprogram_generator().bthreads[i]
                dfs = DFSBThread(f, ess, self.event_list)
                init_s, visited = dfs.run()
                mapper[i] = list(visited)
                init.append(init_s)

            if not explore_graph: # stop before mapping sync statements
                return init, mapper

            init = NodeList(init, tuple(), interrupt_on_trace=self.interrupt_on_trace, predicate=self.predicate)
            visited = set()
            stack = [init]
            while len(stack):
                s = stack.pop()
                if s not in visited:
                    visited.add(s)

                for e in ess.selectable_events([x.data for x in s.nodes if x.data is not None]):
                    new_s = []
                    for i, bt_s in enumerate(s.nodes):
                        s_temp = mapper[i][mapper[i].index(bt_s)]
                        new_s.append(s_temp.transitions[e])
                    new_s = NodeList(new_s, s.prefix + (e, ), interrupt_on_trace=self.interrupt_on_trace, predicate=self.predicate)
                    s.transitions[e] = new_s
                    if new_s not in visited:
                        stack.append(new_s)
            visited = list(visited)
            visited.remove(init)
            visited.insert(0, init)
            return init, visited
        else:
            import random
            ess = self.bprogram_generator().event_selection_strategy
            bprogram = self.bprogram_generator()
            bprogram.setup()
            init = NodeList([Node(tuple(), t) for t in self.tickets_without_bt(bprogram.tickets)], tuple(), interrupt_on_trace=self.interrupt_on_trace, predicate=self.predicate)
            visited = set()
            stack = [init]
            while len(stack):
                s = stack.pop()
                if s not in visited:
                    visited.add(s)
                l = list(ess.selectable_events([x.data for x in s.nodes if x.data is not None]))
                random.shuffle(l)
                for e in l:
                    bprogram = self.bprogram_generator()
                    bprogram.setup()
                    for pre_e in s.prefix:
                        bprogram.advance_bthreads(bprogram.tickets, pre_e)
                    try:
                        bprogram.advance_bthreads(bprogram.tickets, e)
                    except AssertionError:
                        raise BPAssertionError("Assertion error in DFSBProgram", s.prefix + (e,))
                    new_s = NodeList([Node(s.prefix + (e,), t) for t in self.tickets_without_bt(bprogram.tickets)], s.prefix + (e,), interrupt_on_trace=self.interrupt_on_trace, predicate=self.predicate)
                    s.transitions[e] = new_s
                    if (new_s not in visited) and (len(new_s.prefix) <= self.max_trace_length):
                        stack.append(new_s)
            visited = list(visited)
            visited.remove(init)
            visited.insert(0, init)
            return init, visited

    @staticmethod
    def tickets_without_bt(tickets):
        return [dict([(k, v) for k, v in t.items() if k != 'bt']) for t in tickets]



