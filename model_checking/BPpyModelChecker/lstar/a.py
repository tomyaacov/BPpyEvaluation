from bppy import *
data = "data"

@b_thread
def session(i):
    yield {request: BEvent(f"L{i}")}
    while True:
        yield {request: [BEvent(f"A{i}_{j}") for j in range(M)]}

@b_thread
def check_out():
    yield {request: BEvent("LC")}
    yield {waitFor: any_add}
    yield {request: BEvent("C")}
    yield {block: any_add + any_l}

def bug1():
    e = yield {waitFor: BEvent("LC") or any_add}
    if e.name == "LC":
        yield {waitFor: "C"}
        assert False

def bug2():
    e = yield {waitFor: BEvent("LC") or any_add}
    if e.name == "LC":
        assert False

def bug3(i):
    yield {waitFor: BEvent(f"L{i}")}
    e = yield {waitFor: all}
    if e.name.startswith(f"A{i}"):
        assert False



from lstar_dfs import run
from bp_modules import *
import pynusmv
N = 4
M = 1
any_add = [BEvent(f"A{i}_{j}") for i in range(N) for j in range(M)]
any_l = [BEvent(f"L{i}") for i in range(N)]
all = [BEvent(f"A{i}_{j}") for i in range(N) for j in range(M)] + [BEvent(f"L{i}") for i in range(N)] + [BEvent("LC"), BEvent("C")]
event_list = [f"A{i}_{j}" for i in range(N) for j in range(M)] + [f"L{i}" for i in range(N)] + ["LC", "C"]
bt_list = []
bt_list.extend([bthread_to_module(lambda: session(i), f"session_{i}", event_list) for i in range(N)])
bt_list.extend([bthread_to_module(lambda: check_out(), "check_out", event_list)])
run(bt_list, event_list, f"magento_m_{N}_{M}.dot")






