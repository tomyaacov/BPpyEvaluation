from bppy import BEvent
import itertools
import bppy as bp


class PrintBProgramRunnerListener(bp.PrintBProgramRunnerListener):
    def event_selected(self, b_program, event):
        print()
        print("\n".join([",".join([str(event.eval(p[i][j]) == true) for j in range(N)]) for i in range(N)]))


class Assignment(BEvent):
    def __init__(self, kwargs):
        super().__init__("_".join([str(k) + ("T" if v else "F") for k, v in kwargs.items()]))
        self.__dict__.update(kwargs)

    def eval(self, event_set):
        return true if event_set.__contains__(self) else false

def Not(event_set):
    return event_list - event_set


def And(event_sets):
    return set.intersection(*event_sets)


def Or(event_sets):
    return set.union(*event_sets)


def Eq(a, b):
    return And([Implies(a, b), Implies(b, a)])


def Implies(a, b):
    return Or([Not(a), b])



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
    N = 3
    variables_names = [f"p{i}{j}" for i in range(N) for j in range(N)]
    event_list = set([Assignment({k: v for k, v in zip(variables_names, values)}) for values in
                      itertools.product([True, False], repeat=len(variables_names))])
    true = event_list
    false = set()
    p = [[set([e for e in event_list if f"p{i}{j}T" in e.name]) for j in range(N)] for i in range(N)]

    bp_program = bp.BProgram(bthreads=[general()] + [row(i) for i in range(N)] + [col(i) for i in range(N)],
                             event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                             listener=PrintBProgramRunnerListener())

    bp_program.run()
