import os
from stable_baselines3.dqn import MlpPolicy
from stable_baselines3 import DQN, PPO
from sb3_contrib import MaskablePPO
from stable_baselines3.common.monitor import Monitor
from bppy.gym import BPEnv, BPObservationSpace, SimpleBPObservationSpace
import numpy as np
from pancake import init_bprogram, get_event_list, get_action_list

N = 3
M = 1
RUN = "tmp"


class PancakeObservationSpace(BPObservationSpace):
    def __init__(self, dim):
        super().__init__(dim, np.int64, None)

    def bp_state_to_gym_space(self, bthreads_states):
        return np.asarray([x.get("locals", {}).get("i") for x in bthreads_states if "i" in x.get("locals", {})],
                          dtype=self.dtype)


class BPEnvMask(BPEnv):
    def action_masks(self):
        possible_events = self.action_space._possible_actions()
        return [action in possible_events for action in range(self.action_space.n)]


env = BPEnvMask(bprogram_generator=lambda: init_bprogram(N, M),
                action_list=get_action_list(),
                observation_space=PancakeObservationSpace([N+1] * 2),
                reward_function=lambda rewards: sum(filter(None, rewards)))