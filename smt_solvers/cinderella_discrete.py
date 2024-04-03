from bppy import BEvent, EventSet
import itertools
import bppy as bp


N = 5
C = 2
B = 9
A = 5
STEPS = 2


class PrintBProgramRunnerListener(bp.PrintBProgramRunnerListener):
    def event_selected(self, b_program, event):
        print(event.l)


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
    e = yield bp.sync(request=BucketsAssignment([0 for _ in range(N)]))
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



event_list = set([BucketsAssignment(list(values)) for values in
                  itertools.product(list(range(B+1)), repeat=N)])
true = event_list
false = set()

bp_program = bp.BProgram(bthreads=[main(), bucket_limit(), game_ends()],
                         event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())

bp_program.run()
