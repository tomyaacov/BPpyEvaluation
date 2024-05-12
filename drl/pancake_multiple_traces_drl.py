from dfs import DFSBProgram
import argparse
import os
from stable_baselines3 import DQN, SAC
from sb3_contrib import QRDQN
from stable_baselines3.common.monitor import Monitor
from bppy.gym import BPEnv, BPObservationSpace, SimpleBPObservationSpace
import numpy as np
import pandas as pd
from pancake import init_bprogram, get_event_list, get_action_list
from bp_callback_mask_multiple import BPCallbackMaskMultiple
from stable_baselines3.common.utils import get_device
import pickle
import random
import torch

print(torch.cuda.is_available())
print(torch.cuda.device_count())
if torch.cuda.is_available():
    print(torch.cuda.current_device())
    print(torch.cuda.get_device_name(0))

    print("current device:")
    print(get_device())

parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[200, 25, 10, 50_000, "DQN"])
args = parser.parse_args()

N = int(args.parameters[0])
M = int(args.parameters[1])
TESTED_TRACES = int(args.parameters[2])
STEPS = int(args.parameters[3])
MODEL = args.parameters[4]
RUN = str(N) + str(M) + str(STEPS) + MODEL

with open(f'traces_{N}_{M}.pkl', 'rb') as f:
    traces = pickle.load(f)
    CHECK_EVERY = 10

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


class NewBPEnv(BPEnv):

    def step(self, action):
        s, r, d, _, m = super().step(action)
        if m == {"message": "Last event is disabled"}:
            r = -1
        return s, r, d, d, m


env = NewBPEnv(bprogram_generator=lambda: init_bprogram(N, M),
               action_list=get_action_list(),
               observation_space=PancakeObservationSpace([N + 1] * 2),
               reward_function=lambda rewards: sum(filter(None, rewards)))
log_dir = "output/" + RUN + "/"
env = Monitor(env, log_dir)
os.makedirs(log_dir, exist_ok=True)

if MODEL == "DQN":
    model = DQN("MlpPolicy", env, verbose=0)
else:
    model = QRDQN("MlpPolicy", env, verbose=0)
callback_obj = BPCallbackMaskMultiple(traces=traces, check_every=CHECK_EVERY, threshold=(N*(-0.0001))/2)
model.learn(total_timesteps=STEPS, callback=callback_obj)


result = callback_obj.result.split("\n")
columns_names = result[0].split(",")[::2]
result = [x.split(",")[1::2] for x in result]
result = [[float(y) for y in x] for x in result][:-1]
df_results = pd.DataFrame(result, columns=columns_names)

df_results["precision"] = (df_results["TP"] / (df_results["TP"] + df_results["FP"])).fillna(0.0)
df_results["recall"] = (df_results["TP"] / (df_results["TP"] + df_results["FN"])).fillna(0.0)
df_results["precision_w20"] = df_results['precision'][::-1].rolling(20, min_periods=1).mean()[::-1]
df_results["recall_w20"] = df_results['recall'][::-1].rolling(20, min_periods=1).mean()[::-1]
df_results.to_csv(os.path.join(log_dir, "results.csv"), index=False)
print("results saved to", os.path.join(log_dir, "results.csv"))
