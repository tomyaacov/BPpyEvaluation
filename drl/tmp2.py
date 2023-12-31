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

s, _ = env.reset()
print(s)
done = False
while not done:
    a = env.action_space.sample()
    s, r, done, _, _ = env.step(a)
    print(a, s, r, done)

log_dir = "output/" + RUN + "/"
env = Monitor(env, log_dir)
os.makedirs(log_dir, exist_ok=True)
model = MaskablePPO("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=10 ** 4)

observation, _ = env.reset()
print(observation)
while True:
    action_masks = env.action_masks()
    action, _states = model.predict(observation, deterministic=True, action_masks=action_masks)
    observation, reward, done, _, info = env.step(action.item())
    print(action, observation, reward, done)
    if done:
        break
