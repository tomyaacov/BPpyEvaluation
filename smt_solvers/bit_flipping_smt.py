from bppy import BEvent
import itertools
import bppy as bp
from bppy import And, true, false, Not, Implies, Bool, Or, is_true
import timeit
import tracemalloc
import random


random.seed(42)
# Global variables
event_list = None
p = None
N = 3 # Default Number of rows
M = 3 # Default Number of columns

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
        # print()
        # print("\n".join([",".join([str(event.eval(p[i][j]) == true) for j in range(M)]) for i in range(N)]))


class NewSMTEventSelectionStrategy(bp.SMTEventSelectionStrategy):
    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get('waitFor', false), model_completion=True) or event.eval(statement.get('request', false), model_completion=True))

def Eq(a, b):
    return a == b


def row_flipped(i0, e):
    return And([And([Eq(e.eval(v), Not(v) if i == i0 else v) for v in p[i]]) for i in range(N)])


def col_flipped(j0, e):
    return And([And([Eq(e.eval(p[i][j]), Not(p[i][j]) if j == j0 else p[i][j]) for j in range(M)]) for i in range(N)])


@bp.thread
def row(i):
    e = yield bp.sync(waitFor=true)
    while True:
        e = yield bp.sync(request=row_flipped(i, e), waitFor=true)


@bp.thread
def col(i):
    e = yield bp.sync(waitFor=true)
    while True:
        e = yield bp.sync(request=col_flipped(i, e), waitFor=true)




@bp.thread
def general():
    e = yield bp.sync(request=event_list)
    for i in range(N):
        e = yield bp.sync(block=row_flipped(i, e), waitFor=true)
    for j in range(M):
        e = yield bp.sync(block=col_flipped(j, e), waitFor=true)
    yield bp.sync(block=true)

def tracemalloc_stop():
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    total_memory = sum(stat.size for stat in snapshot.statistics("filename"))
    memory_usage = total_memory / 1024 / 1024
    return memory_usage

def run_bit_flipping_smt_bp_program(n=3, m=3):
    global N, M, event_list, true, false, p
    N = n
    M = m
    tracemalloc.start()
    p = [[Bool(f"p{i}{j}") for j in range(M)] for i in range(N)]
    event_list = And([Or([p[i][j], Not(p[i][j])]) for i in range(N) for j in range(M)])  # for requesting all options

    bp_program = bp.BProgram(bthreads=[general()] + [row(i) for i in range(N)] + [col(i) for i in range(M)],
                             event_selection_strategy=NewSMTEventSelectionStrategy(),
                             listener=PrintBProgramRunnerListener())
    start_time = timeit.default_timer()
    bp_program.run()
    end_time = timeit.default_timer()
    memory_usage_smt = tracemalloc_stop()
    execution_time_smt = end_time - start_time
    return execution_time_smt, memory_usage_smt

if __name__ == '__main__':
    import random
    N = 3
    M = 4
    p = [[Bool(f"p{i}{j}") for j in range(M)] for i in range(N)]
    #event_list = And([random.choice([p[i][j], Not(p[i][j])]) for i in range(N) for j in range(N)])  # for requesting all options
    event_list = And([Or([p[i][j], Not(p[i][j])]) for i in range(N) for j in range(M)])  # for requesting all options

    bp_program = bp.BProgram(bthreads=[general()] + [row(i) for i in range(N)] + [col(i) for i in range(M)],
                             event_selection_strategy=NewSMTEventSelectionStrategy(),
                             listener=PrintBProgramRunnerListener())

    bp_program.run()
