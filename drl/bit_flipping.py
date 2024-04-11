import itertools
import bppy as bp
from bppy import And, true, false, Not, Implies, Bool, Or, is_true, Int
from bppy.gym import BPEnv, BPObservationSpace, BPActionSpace
import numpy as np

class PrintBProgramRunnerListener(bp.PrintBProgramRunnerListener):
    def event_selected(self, b_program, event):
        print()
        print("\n".join([",".join([str(event.eval(p[i][j])) for j in range(M)]) for i in range(N)]))


class NewSMTEventSelectionStrategy(bp.SMTEventSelectionStrategy):
    def is_satisfied(self, event, statement):
        return is_true(event.eval(statement.get('waitFor', false), model_completion=True) or event.eval(statement.get('request', false), model_completion=True))

def Eq(a, b):
    return a == b


def row_flipped(i0, e):
    return And([And([Eq(e.eval(v), Not(v) if i == i0 else v) for v in p[i]]) for i in range(N)])


def col_flipped(j0, e):
    return And([And([Eq(e.eval(p[i][j]), Not(p[i][j]) if j == j0 else p[i][j]) for j in range(M)]) for i in range(N)])



@bp.thread
def init():
    e = yield bp.sync(request=And([p[i][j] if (i + j) % 2 else Not(p[i][j]) for i in range(N) for j in range(M)]))


@bp.thread
def bt_env():
    e = yield bp.sync(waitFor=true)
    for _ in range(3):
        i, j = yield bp.choice({(k, v): 1 / (N * M) for k, v in itertools.product(range(N), range(M))})
        yield bp.sync(request=row_flipped(i, e))
        e = yield bp.sync(waitFor=true)
        yield bp.sync(request=col_flipped(j, e))
        e = yield bp.sync(waitFor=true)
    yield bp.sync(block=true)

def flip_row_based_on_action(e):
    return And([Implies(action == i, row_flipped(i, e)) for i in range(N)])

def flip_col_based_on_action(e):
    return And([Implies(action == i, col_flipped(i, e)) for i in range(M)])

@bp.thread
def opponent():
    e = yield bp.sync(waitFor=true)
    for _ in range(3):
        e = yield bp.sync(waitFor=true)
        yield bp.sync(block=Not(flip_row_based_on_action(e)))
        e = yield bp.sync(waitFor=true)
        yield bp.sync(block=Not(flip_col_based_on_action(e)))


@bp.thread
def turn_on():
    while True:
        e = yield bp.sync(waitFor=true)
        for _ in range(3):
            e = yield bp.sync(waitFor=true)
            yield bp.sync(block=Not(flip_row_based_on_action(e)))
            e = yield bp.sync(waitFor=true)
            yield bp.sync(block=Not(flip_col_based_on_action(e)))


@bp.thread
def state_tracker():
    while True:
        e = yield bp.sync(waitFor=true)
        s = []
        for i in range(N):
            for j in range(M):
                s.append(int(e.eval(p[i][j]).__bool__()))


from bp_env_smt import BPEnvSMT

class BitFlipObservationSpace(BPObservationSpace):
    def __init__(self, dim):
        super().__init__(dim, np.int64, None)

    def bp_state_to_gym_space(self, bthreads_states):
        return np.asarray([x.get("locals", {}).get("s") for x in bthreads_states if "s" in x.get("locals", {})][0],
                          dtype=self.dtype)

class ActionSpace(BPActionSpace):
    def _possible_actions(self):
        return [i for i in range(N)]

def init_bprogram(n, m):
    return bp.BProgram(bthreads=[init(), bt_env(), opponent(), state_tracker()],
                       event_selection_strategy=NewSMTEventSelectionStrategy(),
                       listener=PrintBProgramRunnerListener())

def get_action_list(n):
    return [action == i for i in range(n)]


N = 4
M = 4
p = [[Bool(f"p{i}{j}") for j in range(M)] for i in range(N)]
action = Int("action")

class BPEnvMask(BPEnvSMT):
    def action_masks(self):
        possible_events = self.action_space._possible_actions()
        return [action in possible_events for action in range(self.action_space.n)]

# a = init_bprogram(N,M)
# a.run()
env = BPEnvMask(bprogram_generator=lambda: init_bprogram(N,M),
                action_list=get_action_list(N),
                observation_space=BitFlipObservationSpace(N * M),
                reward_function=lambda rewards: sum(filter(None, rewards)))

env.action_space = ActionSpace(get_action_list(N))
obs = env.reset()
print(obs[0])
done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, _, info = env.step(action)
    print(action, obs, reward, done, info)
