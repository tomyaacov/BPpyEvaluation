import os
# from stable_baselines3.dqn import MlpPolicy
# from stable_baselines3 import DQN, PPO
from sb3_contrib import MaskablePPO
from stable_baselines3.common.monitor import Monitor
from bppy.gym import BPEnv, BPObservationSpace, SimpleBPObservationSpace
import numpy as np
from cinderella import init_bprogram, get_event_list, get_action_list
from bp_callback_mask import BPCallbackMask
import warnings

import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("parameters", nargs="*", default=[4, 8, 2, 5, 10_000])
args = parser.parse_args()

A = int(args.parameters[0])
B = int(args.parameters[1])
C = int(args.parameters[2])
N = int(args.parameters[3])
STEPS = int(args.parameters[4])
RUN = str(A) + str(B) + str(C) + str(N) + str(STEPS)


class CinderellaObservationSpace(BPObservationSpace):
    def __init__(self, dim):
        super().__init__(dim, np.int64, None)

    def bp_state_to_gym_space(self, bthreads_states):
        return np.asarray([x.get("locals", {}).get("s") for x in bthreads_states if "s" in x.get("locals", {})][0],
                          dtype=self.dtype)


class BPEnvMask(BPEnv):
    def action_masks(self):
        possible_events = self.action_space._possible_actions()
        return [action in possible_events for action in range(self.action_space.n)]


env = BPEnvMask(bprogram_generator=lambda: init_bprogram(A, B, C, N),
                action_list=get_action_list(N),
                observation_space=CinderellaObservationSpace([B+1] * N),
                reward_function=lambda rewards: sum(filter(None, rewards)))



log_dir = "output/" + RUN + "/"
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    env = Monitor(env, log_dir)
    os.makedirs(log_dir, exist_ok=True)
    model = MaskablePPO("MlpPolicy", env, verbose=0)

    callback = BPCallbackMask(threshold=-0.5)
    model.learn(total_timesteps=STEPS,
                callback=callback)


if model.num_timesteps >= STEPS:
    print("model did not converge")
else:
    print("model converged in", model.num_timesteps, "steps")

model.action_space.bprogram = None
model.save(log_dir + "model")