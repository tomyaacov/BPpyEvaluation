from bppy import BEvent
import itertools
import bppy as bp
from bppy import And, true, false, Not, Implies, Bool, Or, is_true


class PrintBProgramRunnerListener(bp.PrintBProgramRunnerListener):
    def event_selected(self, b_program, event):
        print()
        print("\n".join([",".join([str(event.eval(p[i][j])) for j in range(N)]) for i in range(N)]))


class NewSMTEventSelectionStrategy(bp.SMTEventSelectionStrategy):
    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get('waitFor', false), model_completion=True) or event.eval(statement.get('request', false), model_completion=True))

def Eq(a, b):
    return a == b


def row_flipped(i0, e):
    return And([And([Eq(e.eval(v), Not(v) if i == i0 else v) for v in p[i]]) for i in range(N)])


def col_flipped(j0, e):
    return And([And([Eq(e.eval(p[i][j]), Not(p[i][j]) if j == j0 else p[i][j]) for j in range(N)]) for i in range(N)])


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
    for j in range(N):
        e = yield bp.sync(block=col_flipped(j, e), waitFor=true)
    yield bp.sync(block=true)


if __name__ == '__main__':
    import random
    N = 3
    p = [[Bool(f"p{i}{j}") for j in range(N)] for i in range(N)]
    #event_list = And([random.choice([p[i][j], Not(p[i][j])]) for i in range(N) for j in range(N)])  # for requesting all options
    event_list = And([Or([p[i][j], Not(p[i][j])]) for i in range(N) for j in range(N)])  # for requesting all options

    bp_program = bp.BProgram(bthreads=[general()] + [row(i) for i in range(N)] + [col(i) for i in range(N)],
                             event_selection_strategy=NewSMTEventSelectionStrategy(),
                             listener=PrintBProgramRunnerListener())

    bp_program.run()
