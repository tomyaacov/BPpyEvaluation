from bppy import BEvent, EventSet
import itertools
import bppy as bp


class BucketState(BEvent):
    def __init__(self, l):
        super().__init__("_".join([str(k) + str(v) for k, v in enumerate(l)]))
        self.l = l


class EmptyFrom(BEvent):
    def __init__(self, i):
        super().__init__(f"EmptyFrom{i}")
        self.i = i


stepmother_event_set = EventSet(lambda e: isinstance(e, BucketState))
cinderella_event_set = EventSet(lambda e: isinstance(e, EmptyFrom))


def compute_counter_strategy(e, a, b, c, empty_from):
    new_l = e.l[:]
    if empty_from is not None:
        new_l[empty_from.i] = 0
    if new_l[0] + a >= b:
        new_l[0] = b
        return BucketState(new_l)
    if new_l[c] + a >= b:
        new_l[c] = b
        return BucketState(new_l)
    total = (new_l[0] + new_l[c] + a)
    new_l[0] = min(total // 2, b)
    new_l[c] = min(total - (total // 2), b)
    return BucketState(new_l)


@bp.thread
def main(n):
    yield bp.sync(request=BucketState([0 for _ in range(n)]), block=cinderella_event_set)
    for i in range(10):
        yield bp.sync(block=cinderella_event_set, waitFor=stepmother_event_set)
        yield bp.sync(block=stepmother_event_set, waitFor=cinderella_event_set)
    yield bp.sync(request=BEvent("CinderellaWins"), block=bp.AllExcept(BEvent("CinderellaWins")))
    yield bp.sync(block=bp.All())


@bp.thread
def stepmother(a, b, c):
    e = yield bp.sync(waitFor=stepmother_event_set)
    empty_from = None
    while True:
        e = yield bp.sync(request=compute_counter_strategy(e, a, b, c, empty_from))
        empty_from = yield bp.sync(waitFor=cinderella_event_set)


@bp.thread
def cinderella(n):
    while True:
        yield bp.sync(request=[EmptyFrom(i) for i in range(n)])


@bp.thread
def game_ends(n, b):
    yield bp.sync(waitFor=EventSet(lambda e: isinstance(e, BucketState) and any([e.l[i] == b for i in range(n)])))
    yield bp.sync(request=BEvent("StepmotherWins"), block=bp.AllExcept(BEvent("StepmotherWins")))
    yield bp.sync(block=bp.All())


@bp.thread
def state_tracker():
    while True:
        e = yield bp.sync(waitFor=stepmother_event_set)


def init_bprogram(a, b, c, n):
    bp_program = bp.BProgram(bthreads=[main(n), stepmother(a, b, c), cinderella(n), game_ends(n, b)],
                             event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                             listener=bp.PrintBProgramRunnerListener())
    return bp_program


def get_event_list(b, c, n):
    l = []
    l.extend([EmptyFrom(i) for i in range(n)])
    l.extend([BucketState([values[0]] + ([0]*(c-1)) + [values[1]] + ([0]*(n-c-1))) for values in itertools.product(list(range(b+1)), repeat=2)])
    l.append(BEvent("CinderellaWins"))
    l.append(BEvent("StepmotherWins"))
    return l


def get_action_list(n):
    return [EmptyFrom(i) for i in range(n)]


def get_predicate():
    return lambda l: BEvent("CinderellaWins") in l


if __name__ == '__main__':
    init_bprogram(5, 9, 2, 5).run()