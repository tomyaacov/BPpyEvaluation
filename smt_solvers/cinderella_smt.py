from bppy import *
import bppy as bp
import timeit
import tracemalloc
import random

random.seed(42)
# Global variables
N = 5
C = 2
B = 9
A = 5
STEPS = 2

buckets = [Int(f"b{i}") for i in range(N)]

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
        # print(",".join([str(event.eval(buckets[i])) for i in range(N)]))


def stepmother(prev):
    added_water = Sum([b - prev.eval(b) for b in buckets])
    only_add_water = And([b - prev.eval(b) >= 0 for b in buckets])
    return And(added_water == A,only_add_water )


def cinderella(prev):
    r = list(range(N)) + list(range(N))

    def empty_buckets(rng):
        return And([buckets[j] == 0 if j in rng else buckets[j] == prev.eval(buckets[j]) for j in range(N)])

    return Or([empty_buckets(r[i:i + C]) for i in range(N)])


@bp.thread
def main():
    e = yield bp.sync(request=And([b == 0 for b in buckets]))
    for i in range(STEPS):
        e = yield bp.sync(request=stepmother(e))
        e = yield bp.sync(request=cinderella(e))


@bp.thread
def bucket_limit():
    while True:
        yield bp.sync(block=Or([b > B for b in buckets]))

@bp.thread
def game_ends():
    yield bp.sync(waitFor=Or([b == B for b in buckets]))
    yield bp.sync(block=true)


def tracemalloc_stop():
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    total_memory = sum(stat.size for stat in snapshot.statistics("filename"))
    memory_usage = total_memory / 1024 / 1024
    return memory_usage


def run_cinderella_smt_bp_program(n, c, b, a):
    global N, C, B, A, buckets
    N = n
    C = c
    B = b
    A = a
    tracemalloc.start()
    buckets = [Int(f"b{i}") for i in range(N)]
    bp_program = bp.BProgram(bthreads=[main(), bucket_limit()], # without game_ends scenario
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    start_time = timeit.default_timer()
    bp_program.run()
    end_time = timeit.default_timer()
    memory_usage_smt = tracemalloc_stop()
    execution_time_smt = end_time - start_time
    return execution_time_smt, memory_usage_smt


if __name__ == '__main__':
    bp_program = bp.BProgram(bthreads=[main(), bucket_limit()], # without game_ends scenario
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())

    bp_program.run()
