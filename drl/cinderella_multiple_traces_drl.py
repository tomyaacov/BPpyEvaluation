from dfs import DFSBProgram
import argparse
import os
from stable_baselines3 import DQN, SAC
from sb3_contrib import QRDQN
from stable_baselines3.common.monitor import Monitor
from bppy.gym import BPEnv, BPObservationSpace, SimpleBPObservationSpace
import numpy as np
from cinderella import init_bprogram, get_event_list, get_action_list
from bp_callback_mask_multiple import BPCallbackMaskMultiple
from stable_baselines3.common.utils import get_device
import pickle
import random
import torch

# print(torch.cuda.is_available())
# print(torch.cuda.device_count())
# print(torch.cuda.current_device())
# print(torch.cuda.get_device_name(0))
#
# print("current device:")
# print(get_device())

parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[5, 10, 2, 5, 100, 100_000, "DQN"])
args = parser.parse_args()

A = int(args.parameters[0])
B = int(args.parameters[1])
C = int(args.parameters[2])
N = int(args.parameters[3])
TESTED_TRACES = int(args.parameters[4])
STEPS = int(args.parameters[5])
MODEL = args.parameters[6]
RUN = str(A) + str(B) + str(C) + str(N) + MODEL + str(STEPS)

with open(f'traces_{A}_{B}_{C}_{N}.pkl', 'rb') as f:
    traces = pickle.load(f)
    CHECK_EVERY = 10

random.shuffle(traces)
traces = traces[:TESTED_TRACES]


class CinderellaObservationSpace(BPObservationSpace):
    def __init__(self, dim):
        super().__init__(dim, np.int64, None)

    def bp_state_to_gym_space(self, bthreads_states):
        return np.asarray([x.get("locals", {}).get("s") for x in bthreads_states if "s" in x.get("locals", {})][0],
                          dtype=self.dtype)

# class BPEnvMask(BPEnv):
#     def action_masks(self):
#         possible_events = self.action_space._possible_actions()
#         return [action in possible_events for action in range(self.action_space.n)]


class NewBPEnv(BPEnv):
    def step(self, action):
        s, r, d, _, m = super().step(action)
        if m == {"message": "Last event is disabled"}:
            r = -1
        return s, r, d, d, m


env = NewBPEnv(bprogram_generator=lambda: init_bprogram(A, B, C, N),
                action_list=get_action_list(N),
                observation_space=CinderellaObservationSpace([B+1] * N),
                reward_function=lambda rewards: sum(filter(None, rewards)))

log_dir = "output/" + RUN + "/"
env = Monitor(env, log_dir)
os.makedirs(log_dir, exist_ok=True)

if MODEL == "DQN":
    model = DQN("MlpPolicy", env, verbose=0)
else:
    model = QRDQN("MlpPolicy", env, verbose=0)
callback_obj = BPCallbackMaskMultiple(traces=traces, check_every=CHECK_EVERY, threshold=-0.5)
model.learn(total_timesteps=STEPS, callback=callback_obj)

print("Final results:")
print(callback_obj.result)
