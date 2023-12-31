import bppy as bp

any_addition = {bp.BEvent("DryMixture"), bp.BEvent("WetMixture"), bp.BEvent("AddBlueberries")}
any_mixture_addition = {bp.BEvent("DryMixture"), bp.BEvent("WetMixture")}
any_thickness = bp.EventSet(lambda e: e.name == "Thickness")


@bp.thread
def add_dry_mixture(n):
    for i in range(n):
        yield bp.sync(request=bp.BEvent("DryMixture"))
    i += 1
    yield bp.sync(waitFor=bp.EventSet(lambda e: False))


@bp.thread
def add_wet_mixture(n):
    for i in range(n):
        yield bp.sync(request=bp.BEvent("WetMixture"))
    i += 1
    yield bp.sync(waitFor=bp.EventSet(lambda e: False))


@bp.thread
def thickness_meter():
    thickness = 0
    e = None
    while True:
        e = yield bp.sync(waitFor=any_mixture_addition)
        if e.name == "DryMixture":
            thickness += 1
        else:
            thickness -= 1
        e = None
        yield bp.sync(request=bp.BEvent("Thickness", {"thickness": thickness}), block=any_addition)


@bp.thread
def range_arbiter(bound):
    thickness = 0
    e = None
    while True:
        e = yield bp.sync(waitFor=any_thickness)
        thickness = e.data["thickness"]
        e = None
        if thickness >= bound:
            yield bp.sync(block=bp.BEvent("DryMixture"), waitFor=any_mixture_addition)
        elif thickness <= -bound:
            yield bp.sync(block=bp.BEvent("WetMixture"), waitFor=any_mixture_addition)
        else:
            yield bp.sync(waitFor=any_mixture_addition)


@bp.thread
def blueberries():
    yield bp.sync(request=bp.BEvent("AddBlueberries"), localReward=-0.001)
    yield bp.sync(request=bp.BEvent("DoneBlueberries"), block=bp.AllExcept(bp.BEvent("DoneBlueberries")), localReward=1)


@bp.thread
def enough_batter(n):
    for j in range(int((n * 6) / 4)):
        yield bp.sync(waitFor=any_mixture_addition, block=bp.BEvent("AddBlueberries"))


@bp.thread
def batter_thin_enough():
    thickness = 0
    e = None
    while True:
        if thickness >= 0:
            e = yield bp.sync(waitFor=any_thickness, block=bp.BEvent("AddBlueberries"))
        else:
            e = yield bp.sync(waitFor=any_thickness)
        thickness = e.data["thickness"]
        e = None


def init_bprogram(n, m):
    return bp.BProgram(bthreads=[add_dry_mixture(n),
                                 add_wet_mixture(n),
                                 thickness_meter(),
                                 range_arbiter(m),
                                 blueberries(),
                                 enough_batter(n),
                                 batter_thin_enough()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                       listener=bp.PrintBProgramRunnerListener())


def get_event_list(n):
    return ([bp.BEvent("DryMixture"), bp.BEvent("WetMixture"), bp.BEvent("AddBlueberries"), bp.BEvent("DoneBlueberries")] +
            [bp.BEvent("Thickness", {"thickness": i}) for i in range(-n, n+1)])


def get_action_list():
    return [bp.BEvent("DryMixture"), bp.BEvent("WetMixture"), bp.BEvent("AddBlueberries"), bp.BEvent("DoneBlueberries")]


if __name__ == '__main__':
    init_bprogram(3, 1).run()

