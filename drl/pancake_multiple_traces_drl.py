from dfs import DFSBProgram
import argparse
import os
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from bppy.gym import BPEnv, BPObservationSpace, SimpleBPObservationSpace
import numpy as np
from pancake import init_bprogram, get_event_list, get_action_list
from bp_callback_mask_multiple import BPCallbackMaskMultiple
from stable_baselines3.common.utils import get_device
import pickle
import random

print("current device:")
print(get_device())

parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[10, 5, 100, "tmp"])
args = parser.parse_args()

N = int(args.parameters[0])
M = int(args.parameters[1])
TESTED_TRACES = int(args.parameters[2])
RUN = str(N) + str(M) + args.parameters[3]

with open('traces.pkl', 'rb') as f:
    traces = pickle.load(f)

random.shuffle(traces)
traces = traces[:TESTED_TRACES]

class PancakeObservationSpace(BPObservationSpace):
    def __init__(self, dim):
        super().__init__(dim, np.int64, None)

    def bp_state_to_gym_space(self, bthreads_states):
        return np.asarray([x.get("locals", {}).get("i") for x in bthreads_states if "i" in x.get("locals", {})],
                          dtype=self.dtype)


# class BPEnvMask(BPEnv):
#     def action_masks(self):
#         possible_events = self.action_space._possible_actions()
#         return [action in possible_events for action in range(self.action_space.n)]


env = BPEnv(bprogram_generator=lambda: init_bprogram(N, M),
            action_list=get_action_list(),
            observation_space=PancakeObservationSpace([N + 1] * 2),
            reward_function=lambda rewards: sum(filter(None, rewards)))

log_dir = "output/" + RUN + "/"
env = Monitor(env, log_dir)
os.makedirs(log_dir, exist_ok=True)
model = DQN("MlpPolicy", env, verbose=0)
callback_obj = BPCallbackMaskMultiple(traces=traces)
model.learn(total_timesteps=1_000_000, callback=callback_obj)

print(callback_obj.result)
