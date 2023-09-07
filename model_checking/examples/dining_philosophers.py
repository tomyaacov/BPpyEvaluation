from bppy import BEvent, b_thread, waitFor, request, block, BProgram, PrintBProgramRunnerListener, \
    SimpleEventSelectionStrategy
must_finish = "must_finish"
data = "data"


def set_dp_bprogram(n):
    global PHILOSOPHER_COUNT, any_take, any_put, any_take_semaphore, any_release_semaphore, all_events

    PHILOSOPHER_COUNT = n

    any_take = dict(
        [(i, [BEvent(f"T{i}R"), BEvent(f"T{(i + 1) % PHILOSOPHER_COUNT}L")]) for i in range(PHILOSOPHER_COUNT)])
    any_put = dict(
        [(i, [BEvent(f"P{i}R"), BEvent(f"P{(i + 1) % PHILOSOPHER_COUNT}L")]) for i in range(PHILOSOPHER_COUNT)])
    any_take_semaphore = [BEvent(f"TS{i}") for i in range(PHILOSOPHER_COUNT)]
    any_release_semaphore = [BEvent(f"RS{i}") for i in range(PHILOSOPHER_COUNT)]
    all_events = [BEvent(f"T{i}R") for i in range(PHILOSOPHER_COUNT)] + \
                 [BEvent(f"T{i}L") for i in range(PHILOSOPHER_COUNT)] + \
                 [BEvent(f"P{i}R") for i in range(PHILOSOPHER_COUNT)] + \
                 [BEvent(f"P{i}L") for i in range(PHILOSOPHER_COUNT)] + \
                 [BEvent(f"TS{i}") for i in range(PHILOSOPHER_COUNT)] + \
                 [BEvent(f"RS{i}") for i in range(PHILOSOPHER_COUNT)]


@b_thread
def philosopher(i):
    while True:
        for j in range(2):
            yield {request: [BEvent(f"T{i}R"), BEvent(f"T{i}L")], data: locals()}
        for j in range(2):
            yield {request: [BEvent(f"P{i}R"), BEvent(f"P{i}L")], data: locals()}


@b_thread
def fork(i):
    while True:
        e, cannot_put = None, None
        e = yield {waitFor: any_take[i], block: any_put[i], data: locals()}
        cannot_put = BEvent(f"P{(i + 1) % PHILOSOPHER_COUNT}L") if e.name.endswith("R") else BEvent(f"P{i}R")
        yield {waitFor: any_put[i], block: any_take[i] + [cannot_put], data: locals()}

# A taken fork will eventually be released
@b_thread
def fork_eventually_released(i):
    while True:
        yield {waitFor: any_take[i]}
        yield {waitFor: any_put[i], must_finish: True}

@b_thread
def semaphore():
    while True:
        yield {waitFor: any_take_semaphore}
        yield {waitFor: any_release_semaphore, block: any_take_semaphore}

@b_thread
def take_semaphore(i):
    while True:
        yield {request: BEvent(f"TS{i}"), block: [BEvent(f"T{i}R"), BEvent(f"T{i}L")], data: locals()}
        for j in range(2):
            yield {waitFor: [BEvent(f"T{i}R"), BEvent(f"T{i}L")], data: locals()}
        yield {request: BEvent(f"RS{i}"), block: [BEvent(f"P{i}R"), BEvent(f"P{i}L")], data: locals()}
        for j in range(2):
            yield {waitFor: [BEvent(f"P{i}R"), BEvent(f"P{i}L")], data: locals()}





