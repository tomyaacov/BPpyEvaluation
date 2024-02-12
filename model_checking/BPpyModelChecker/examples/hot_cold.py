#from bppy.model.b_thread import b_thread
from bppy.model.b_event import BEvent
#from bppy.model.sync_statement import waitFor, request, block
import bppy as bp

must_finish = "must_finish"
data = "data"


def set_bprogram(n, m):
    global N, M, event_list, any_portion, any_cold
    N = n
    M = m
    event_list = ["HOT"] + ["COLD" + str(i) for i in range(M)]
    any_portion = [BEvent("COLD" + str(i)) for i in range(M)] + [BEvent("HOT")]
    any_cold = [BEvent("COLD" + str(i)) for i in range(M)]


@bp.thread
def add_a():
    for i in range(N):
        yield bp.sync(request=BEvent("HOT"), must_finish=True, data=locals())


@bp.thread
def add_b(C):
    for i in range(N):
        yield bp.sync(request=BEvent(C), must_finish=False, data=locals())


@bp.thread
def control():
    while True:
        yield bp.sync(waitFor=BEvent("HOT"), must_finish=False, data=locals())
        yield bp.sync(waitFor=any_portion, block=BEvent("HOT"), must_finish=False, data=locals())


@bp.thread
def control2():
    e = yield bp.sync(waitFor=any_portion)
    while True:
        if e in any_cold:
            e = yield bp.sync(waitFor=any_portion, block=any_cold, must_finish=False)
        else:
            e = yield bp.sync(waitFor=any_portion, block=BEvent("HOT"), must_finish=False)




