from bppy import BEvent, EventSet
import itertools
import bppy as bp
import timeit
import tracemalloc
import random


random.seed(42)
# Global variables
event_list = None
true = None
false = None
N = 5
C = 2
B = 9
A = 5
STEPS = 2


class PrintBProgramRunnerListener(bp.PrintBProgramRunnerListener):
    def starting(self, b_program):
        pass
        """
        Prints "STARTED" when the BProgram execution is about to start.
        """
        # print("STARTED")

    def ended(self, b_program):
        pass
        """
        Prints "ENDED" when the BProgram execution is about to start.
        """
        # print("ENDED")

    def event_selected(self, b_program, event):
        pass
        # print(event.l)


class BucketsAssignment(BEvent):
    def __init__(self, l):
        super().__init__("_".join([str(k) + str(v) for k, v in enumerate(l)]))
        self.l = l

    def eval(self, event_set):
        return true if event_set.__contains__(self) else false


def stepmother(e):
    l = []
    for new_e in event_list:
        if all([x-y >= 0 for x, y in zip(new_e.l, e.l)]):
            if sum([x-y for x, y in zip(new_e.l, e.l)]) == A:
                l.append(new_e)
    return l

def cinderella(e):
    r = list(range(N)) + list(range(N))

    def empty(i):
        return BucketsAssignment([0 if j in r[i:i + C] else e.l[j] for j in range(N)])

    return [empty(i) for i in range(N)]




@bp.thread
def main():
    buckets_assignment = BucketsAssignment([0 for _ in range(N)])
    e = yield bp.sync(request=buckets_assignment)
    for i in range(STEPS):
        e = yield bp.sync(request=stepmother(e))
        e = yield bp.sync(request=cinderella(e))


@bp.thread
def bucket_limit():
    while True:
        yield bp.sync(block=false)

@bp.thread
def game_ends():
    yield bp.sync(waitFor=EventSet(lambda e: any([e.l[i] == B for i in range(N)])))
    yield bp.sync(block=bp.All())


def tracemalloc_stop():
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    total_memory = sum(stat.size for stat in snapshot.statistics("filename"))
    memory_usage = total_memory / 1024 / 1024
    return memory_usage


def run_cinderella_discrete_bp_program( n, c, b,  a ):
    global N, C, B, A, event_list, true, false
    N = n
    C = c
    B = b
    A = a
    event_list = set([BucketsAssignment(list(values)) for values in
                      itertools.product(list(range(B + 1)), repeat=N)])
    true = event_list
    false = set()
    bp_program = bp.BProgram(bthreads=[main(), bucket_limit()], # without game_ends scenario
                             event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                             listener=PrintBProgramRunnerListener())
    start_time = timeit.default_timer()
    tracemalloc.start()
    bp_program.run()
    end_time = timeit.default_timer()
    memory_usage_discrete = tracemalloc_stop()
    execution_time_discrete = end_time - start_time
    return execution_time_discrete, memory_usage_discrete

if __name__ == '__main__':
    event_list = set([BucketsAssignment(list(values)) for values in
                      itertools.product(list(range(B+1)), repeat=N)])
    true = event_list
    false = set()

    bp_program = bp.BProgram(bthreads=[main(), bucket_limit(), game_ends()],
                             event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                             listener=PrintBProgramRunnerListener())

    bp_program.run()
