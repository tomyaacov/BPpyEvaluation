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
        print()
        print("\n".join([",".join([str(event.eval(p[i][j])) for j in range(M)]) for i in range(N)]))


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
def init():
    e = yield bp.sync(request=And([p[i][j] if (i + j) % 2 else Not(p[i][j]) for i in range(N) for j in range(M)]))

@bp.thread
def env():
    e = yield bp.sync(waitFor=true)
    for i in range(3):
        i, j = yield bp.choice({(k, v): 1 / (N * M) for k, v in itertools.product(range(N), range(M))})
        yield bp.sync(request=row_flipped(i, e))
        e = yield bp.sync(waitFor=true)
        yield bp.sync(request=col_flipped(j, e))
        e = yield bp.sync(waitFor=true)

@bp.thread
def opponent():
    e = yield bp.sync(waitFor=true)
    for i in range(3):
        i, j = yield bp.choice({(k, v): 1 / (N * M) for k, v in itertools.product(range(N), range(M))})
        e = yield bp.sync(waitFor=true)
        yield bp.sync(request=row_flipped(i, e))
        e = yield bp.sync(waitFor=true)
        yield bp.sync(request=col_flipped(j, e))







if __name__ == '__main__':
    import random
    N = 3
    M = 4
    p = [[Bool(f"p{i}{j}") for j in range(M)] for i in range(N)]
    #event_list = And([random.choice([p[i][j], Not(p[i][j])]) for i in range(N) for j in range(N)])  # for requesting all options
    event_list = And([Or([p[i][j], Not(p[i][j])]) for i in range(N) for j in range(M)])  # for requesting all options

    bp_program = bp.BProgram(bthreads=[init(), env(), opponent()],
                             event_selection_strategy=NewSMTEventSelectionStrategy(),
                             listener=PrintBProgramRunnerListener())

    bp_program.run()
