import itertools
import bppy as bp
from bppy import And, true, false, Not, Implies, Bool, Or, is_true, Int
from bppy.gym import BPEnv, BPObservationSpace, BPActionSpace
from stable_baselines3.common.monitor import Monitor
import numpy as np
from bppy.utils.z3helper import *
import warnings

import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[2, 2, 10_000])
args = parser.parse_args()


N = int(args.parameters[0])
M = int(args.parameters[1])
STEPS = int(args.parameters[2])
RUN = str(N) + str(M) + str(STEPS)


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
def timer():
    for _ in range(10):
        yield bp.sync(waitFor=true, block=done)
    yield bp.sync(block=Not(done))



@bp.thread
def bt_env():
    e = yield bp.sync(waitFor=true)
    while True:
        i, j = yield bp.choice({(k, v): 1 / (N * M) for k, v in itertools.product(range(N), range(M))})
        yield bp.sync(request=row_flipped(i, e))
        e = yield bp.sync(waitFor=true)
        yield bp.sync(request=col_flipped(j, e))
        e = yield bp.sync(waitFor=true)

def flip_row_based_on_action(e):
    return And([Implies(action == i, row_flipped(i, e)) for i in range(N)])

def flip_col_based_on_action(e):
    return And([Implies(action == i, col_flipped(i, e)) for i in range(M)])

@bp.thread
def controller():
    e = yield bp.sync(waitFor=true)
    while True:
        e = yield bp.sync(waitFor=true)
        yield bp.sync(block=Not(flip_row_based_on_action(e)), waitFor=true)
        e = yield bp.sync(waitFor=true)
        yield bp.sync(block=Not(flip_col_based_on_action(e)), waitFor=true)


@bp.thread
def state_tracker():
    c = 0
    while True:
        e = yield bp.sync(waitFor=true)
        s = []
        for i in range(N):
            for j in range(M):
                s.append(int(is_true(e.eval(p[i][j]))))
        c += 1
        s.append((c//2)%2)

def count_reward(e_0, e_1):
    return 2**sum([int(is_true(e_1.eval(p[i][j])) and not is_true(e_0.eval(p[i][j]))) for i in range(N) for j in range(M)])

@bp.thread
def reward():
    e_0 = yield bp.sync(waitFor=true)
    e_1 = yield bp.sync(waitFor=true)
    while True:
        e_0 = yield bp.sync(waitFor=true, localReward=count_reward(e_0, e_1))
        e_1 = yield bp.sync(waitFor=true, localReward=count_reward(e_1, e_0))


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
    return bp.BProgram(bthreads=[init(), timer(), bt_env(), controller(), state_tracker(), reward()],
                       event_selection_strategy=NewSMTEventSelectionStrategy(),
                       listener=PrintBProgramRunnerListener())

def get_action_list(n):
    return [action == i for i in range(n)]



p = [[Bool(f"p{i}{j}") for j in range(M)] for i in range(N)]
action = Int("action")
done = Bool("done")

class BPEnvMask(BPEnvSMT):
    def action_masks(self):
        possible_events = self.action_space._possible_actions()
        return [action in possible_events for action in range(self.action_space.n)]

# a = init_bprogram(N,M)
# a.run()
env = BPEnvMask(bprogram_generator=lambda: init_bprogram(N,M),
                action_list=get_action_list(N),
                observation_space=BitFlipObservationSpace([2]*(N * M + 1)),
                reward_function=lambda rewards: sum(filter(None, rewards)))

env.action_space = ActionSpace(get_action_list(N))
obs = env.reset()
print(obs[0])
env_done = False
while not env_done:
    a = env.action_space.sample()
    obs, reward, env_done, _, info = env.step(a)
    print(a, obs, reward, env_done, info)
# log_dir = "output/" + RUN + "/"
# with warnings.catch_warnings():
#     from stable_baselines3 import PPO
#     env = Monitor(env, log_dir)
#     os.makedirs(log_dir, exist_ok=True)
#     mdl = PPO("MlpPolicy", env, verbose=1)
#     mdl.learn(total_timesteps=STEPS)