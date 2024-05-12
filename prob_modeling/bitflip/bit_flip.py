from bppy import BEvent
import itertools
import bppy as bp
from bppy.analysis.bprogram_converter import BProgramConverter

def param_combs(low_n = 2, low_m = 2, upper_n=4, upper_m=5):
    combs = itertools.product(range(low_n,upper_n+1), range(low_m,upper_m+1))
    combs = [(n, m) for n, m in combs if n <= m]
    return combs

            
def generate_model(N, M, mode=bp.execution_thread):
    class EvaluatorListener(bp.PrintBProgramRunnerListener):
        def starting(self, b_program):
            self.events = []
        def ended(self, b_program):
            pass
        def event_selected(self, b_program, event):
            self.events.append(','.join([f'{i}{j}T' if f"p{i}{j}T"
                                in event.name else f'{i}{j}F' for j in range(M) for i in range(N)]))
            if len(self.events) == 20:
                raise TimeoutError()
    
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
        return And([And([Eq(e.eval(p[i][j]), Not(p[i][j]) if j == j0 else p[i][j]) for j in range(M)]) for i in range(N)])

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


    @mode
    def init():
        M0_init = true
        diagonal_bits = yield bp.choice({True: 0.6, False: 0.4}, repeat=N)
        diagonal_bits = [true if bit else false for bit in diagonal_bits]
        for i in range(N):
            for j in range(M):
                if i == j:
                    bit = diagonal_bits[i]
                else:
                    bit = false
                M0_init = And([M0_init, Eq(p[i][j], bit)])
        yield bp.sync(request=M0_init)


    @mode
    def general():
        e = yield bp.sync(waitFor=true)
        for i in range(N):
            e = yield bp.sync(
                block=Or([row_flipped(i, e), col_flipped(i, e)]), # request both?
                waitFor=true)
        yield bp.sync(block=true)

    # N always <= M
    assert N <= M

    variables_names = [f"p{i}{j}" for i in range(N) for j in range(M)]
    event_list = set([Assignment({k: v for k, v in zip(variables_names, values)}) for values in
                        itertools.product([True, False], repeat=len(variables_names))])
    true = event_list
    false = set()
    p = [[set([e for e in event_list if f"p{i}{j}T" in e.name]) for j in range(M)] for i in range(N)]

    def bp_gen():
        return bp.BProgram(bthreads=[init(), general()] + [row(i) for i in range(N)] + [col(i) for i in range(M)],
                            event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                            listener=EvaluatorListener())
        
    if mode == bp.analysis_thread:
        return bp_gen, event_list
        # converter = BProgramConverter(bp_gen, event_list,
        #                             ["begin", "general"] + [f"row{i}" for i in range(N)] + [f"col{i}" for i in
        #                                                                                     range(M)])
        # converter.to_prism("bitflip.pm")

    else:
        return bp_gen

if __name__ == "__main__":
    a = generate_model(2, 2)()
    a.run()
    print(a.listener.events)