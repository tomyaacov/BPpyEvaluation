from bppy import BEvent
import itertools
import bppy as bp

mode = bp.analysis_thread
#mode = bp.execution_thread
#mode = bp.thread

class PrintBProgramRunnerListener(bp.PrintBProgramRunnerListener):
    def event_selected(self, b_program, event):
        print()
        print("\n".join([",".join([str(event.eval(p[i][j]) == true) for j in range(N)]) for i in range(N)]))


# class Assignment(BEvent):
#     def __init__(self, kwargs):
#         super().__init__("_".join([str(k) + ("T" if v else "F") for k, v in kwargs.items()]))
#         self.__dict__.update(kwargs)
#
#     def eval(self, event_set):
#         return true if event_set.__contains__(self) else false
#
# def Not(event_set):
#     return event_list - event_set
#
#
# def And(event_sets):
#     return set.intersection(*event_sets)
#
#
# def Or(event_sets):
#     return set.union(*event_sets)
#
#
# def Eq(a, b):
#     return And([Implies(a, b), Implies(b, a)])
#
#
# def Implies(a, b):
#     return Or([Not(a), b])
def Eq(a, b):
    return a == b


def row_flipped(i0, e):
    return And([And([Eq(e.eval(v), Not(v) if i == i0 else v) for v in p[i]]) for i in range(N)])


def col_flipped(j0, e):
    return And([And([Eq(e.eval(p[i][j]), Not(p[i][j]) if j == j0 else p[i][j]) for j in range(N)]) for i in range(N)])


@mode
def row(i):
    e = yield bp.sync(waitFor=true)
    while True:
        e = yield bp.sync(request=row_flipped(i, e), waitFor=true)


@mode
def col(i):
    e = yield bp.sync(waitFor=true)
    while True:
        e = yield bp.sync(request=col_flipped(i, e), waitFor=true)
import random
@mode
def init():
    M0_init = true
    for i in range(N):
        for j in range(N):
            bit = yield bp.choice({True: 0.5, False: 0.5})
            bit = true if bit else false
            M0_init = And([M0_init, Eq(p[i][j], bit)])
    yield bp.sync(request=M0_init)


@mode
def general():
    e = yield bp.sync(waitFor=true)
    for i in range(N):
        e = yield bp.sync(block=Or([row_flipped(i, e),col_flipped(i, e)]), waitFor=true)
    yield bp.sync(block=true)

from bppy.utils.z3helper import *
def generate_events():
    l = []
    for values in itertools.product([true, false], repeat=N**2):
        s = Solver()
        for i in range(N):
            for j in range(N):
                s.add(Eq(p[i][j], values[i*N+j]))
        if s.check() == sat:
            m = s.model()
            m.name = str("_".join(["T" if v == true else "F" for v in values]))
            l.append(m)
        else:
            raise ValueError("Unsat!")
    return l



from bppy.analysis.bprogram_converter import BProgramConverter
N = 2
p = [[Bool(f"p{i}{j}") for j in range(N)] for i in range(N)]
event_list = generate_events()
class NewSMTEventSelectionStrategy(bp.SMTEventSelectionStrategy):
    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get('waitFor', false), model_completion=True) or event.eval(
            statement.get('request', false), model_completion=True))


def bp_gen():
    return bp.BProgram(bthreads=[init()],#[init(), general()] + [row(i) for i in range(N)] + [col(i) for i in range(N)],
                        event_selection_strategy=NewSMTEventSelectionStrategy(),
                        listener=bp.PrintBProgramRunnerListener())



if mode == bp.analysis_thread:
    converter = BProgramConverter(bp_gen, event_list,
                                      ["init"])#["init", "general"] + [f"row{i}" for i in range(N)] + [f"col{i}" for i in range(N)])
    content = converter.to_prism()
    with open("bit_flip.prism", "w") as f:
        f.write(content)
else:
    bp_gen().run()


