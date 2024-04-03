from bppy import *
import bppy as bp

N = 5
C = 2
B = 9
A = 5
STEPS = 2

buckets = [Int(f"b{i}") for i in range(N)]

class PrintBProgramRunnerListener(bp.PrintBProgramRunnerListener):
    def event_selected(self, b_program, event):
        print(",".join([str(event.eval(buckets[i])) for i in range(N)]))


def stepmother(e):
    return And(Sum([b - e.eval(b) for b in buckets]) == A,
               And([b - e.eval(b) >= 0 for b in buckets]))


def cinderella(e):
    r = list(range(N)) + list(range(N))

    def empty(i):
        return And([buckets[j] == 0 if j in r[i:i + C] else buckets[j] == e.eval(buckets[j]) for j in range(N)])

    return Or([empty(i) for i in range(N)])


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



bp_program = bp.BProgram(bthreads=[main(), bucket_limit(), game_ends()],
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())

bp_program.run()
