import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread

state = "state"
params = {
    "n": None,  # number of Cs and Hs
    "k": None,  # block k + 1 Hs in a row
    "m": None  #
}


@b_thread
def add_hot():
    for i in range(params["n"]):
        yield {request: bp.BEvent("HOT"), localReward: -0.001}
    yield {request: bp.BEvent("DONE_HOT"), localReward: 1}

@b_thread
def add_cold(name):
    for i in range(params["n"]):
        yield {request: bp.BEvent("COLD" + name)}

@b_thread
def control():
    while True:
        for j in range(0, params["k"]):
            i = 0
            e = yield {waitFor: bp.All()}
            if e.name != "HOT":
                break
        if e.name == "HOT":
            i = 1
            yield {waitFor: bp.BEvent("COLD0"), block: bp.BEvent("HOT")}


def init_bprogram():
    return bp.BProgram(bthreads=[add_hot()] + [add_cold(str(x)) for x in range(params["m"])] + [control()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                       listener=bp.PrintBProgramRunnerListener())


def get_event_list():
    return [bp.BEvent("HOT")] + [bp.BEvent("COLD" + str(x)) for x in range(params["m"])]+ [bp.BEvent("DONE_HOT")]


if __name__ == '__main__':
    params["n"] = 2
    params["k"] = 1
    params["m"] = 3
    init_bprogram().run()
