import bppy as bp

any_addition = {bp.BEvent("DryMixture"), bp.BEvent("WetMixture"), bp.BEvent("AddBlueberries")}
any_mixture_addition = {bp.BEvent("DryMixture"), bp.BEvent("WetMixture")}
any_thickness = bp.EventSet(lambda e: e.name.startswith("Thickness"))


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
    e = None
    while True:
        e = yield bp.sync(waitFor=any_mixture_addition)
        if e.name == "DryMixture":
            yield bp.sync(request=bp.BEvent("ThicknessUp"), block=any_addition)
        else:
            yield bp.sync(request=bp.BEvent("ThicknessDown"), block=any_addition)
        e = None


@bp.thread
def range_arbiter(bound, n):
    thickness = 0
    e = None
    while True:
        e = yield bp.sync(waitFor=any_thickness)
        thickness += 1 if e.name == "ThicknessUp" else -1
        thickness = max(-n, min(n, thickness))  # TODO: resolve this
        e = None
        if abs(thickness) >= bound:
            yield bp.sync(block=bp.BEvent("DryMixture") if thickness > 0 else bp.BEvent("WetMixture"),
                          waitFor=any_mixture_addition)
        else:
            yield bp.sync(waitFor=any_mixture_addition)


@bp.thread
def blueberries():
    yield bp.sync(request=bp.BEvent("AddBlueberries"), localReward=-0.0001)
    yield bp.sync(waitFor=bp.All(), localReward=1)


@bp.thread
def enough_batter(n):
    for j in range(int((n * 6) / 4)):
        yield bp.sync(waitFor=any_mixture_addition, block=bp.BEvent("AddBlueberries"))


@bp.thread
def batter_thin_enough(n):
    thickness = 0
    e = None
    while True:
        if thickness >= 0:
            e = yield bp.sync(waitFor=any_thickness, block=bp.BEvent("AddBlueberries"))
        else:
            e = yield bp.sync(waitFor=any_thickness)
        thickness += 1 if e.name == "ThicknessUp" else -1
        thickness = max(-n, min(n, thickness))  # TODO: resolve this
        e = None


def init_bprogram(n, m):
    return bp.BProgram(bthreads=[add_dry_mixture(n),
                                 add_wet_mixture(n),
                                 thickness_meter(),
                                 range_arbiter(m,n),
                                 blueberries(),
                                 enough_batter(n),
                                 batter_thin_enough(n)],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                       listener=bp.PrintBProgramRunnerListener())


def get_event_list():
    return [bp.BEvent("DryMixture"), bp.BEvent("WetMixture"), bp.BEvent("AddBlueberries"), bp.BEvent("ThicknessUp"), bp.BEvent("ThicknessDown")]


def get_action_list():
    return [bp.BEvent("DryMixture"), bp.BEvent("WetMixture"), bp.BEvent("AddBlueberries")]


def get_predicate():
    return lambda l: bp.BEvent("AddBlueberries") in l

if __name__ == '__main__':
    init_bprogram(3, 1).run()

