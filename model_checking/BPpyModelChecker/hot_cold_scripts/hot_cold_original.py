from bppy.model.b_thread import b_thread
from bppy.model.b_event import BEvent
from bppy.model.sync_statement import waitFor, request, block
must_finish = "must_finish"
data = "data"
N = 5
@b_thread
def add_a():
    yield {waitFor: BEvent("Start"), must_finish: False, data: locals()}
    for i in range(N):
        yield {request: BEvent("HOT"), must_finish: True, data: locals()}

@b_thread
def add_b():
    yield {waitFor: BEvent("Start"), must_finish: False, data: locals()}
    for i in range(N):
        yield {request: BEvent("COLD"), must_finish: False, data: locals()}
    while True:
        yield {request: BEvent("IDLE"), must_finish: False, data: locals()}

@b_thread
def control():
    yield {request: BEvent("Start"), must_finish: False, data: locals()}
    while True:
        yield {waitFor: BEvent("HOT"), must_finish: False, data: locals()}
        yield {waitFor: BEvent("COLD"), block: BEvent("HOT"), must_finish: False, data: locals()}