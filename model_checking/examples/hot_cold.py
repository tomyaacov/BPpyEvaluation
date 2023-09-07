from bppy.model.b_thread import b_thread
from bppy.model.b_event import BEvent
from bppy.model.sync_statement import waitFor, request, block

must_finish = "must_finish"
data = "data"


def set_bprogram(n, m):
    global N, M, event_list, any_portion, any_cold
    N = n
    M = m
    event_list = ["HOT"] + ["COLD" + str(i) for i in range(M)]
    any_portion = [BEvent("COLD" + str(i)) for i in range(M)] + [BEvent("HOT")]
    any_cold = [BEvent("COLD" + str(i)) for i in range(M)]


@b_thread
def add_a():
    for i in range(N):
        yield {request: BEvent("HOT"), must_finish: True, data: locals()}


@b_thread
def add_b(C):
    for i in range(N):
        yield {request: BEvent(C), must_finish: False, data: locals()}


@b_thread
def control():
    while True:
        yield {waitFor: BEvent("HOT"), must_finish: False, data: locals()}
        yield {waitFor: any_portion, block: BEvent("HOT"), must_finish: False, data: locals()}


@b_thread
def control2():
    e = yield {waitFor: any_portion}
    while True:
        if e in any_cold:
            e = yield {waitFor: any_portion, block: any_cold, must_finish: False}
        else:
            e = yield {waitFor: any_portion, block: BEvent("HOT"), must_finish: False}



