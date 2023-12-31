
import gymnasium as gym
# from gym import error, spaces, utils, GoalEnv
from gymnasium.utils import seeding
from gymnasium import spaces
import numpy as np
# from bp.bp_action_space import BPActionSpace
import random


class BPEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.bprogram_generator = None
        self.action_space = None
        self.observation_space = None
        self.last_state = None
        self.bprogram = None
        self.np_random = None
        self.last_event = None
        self.hot_states = None
        self.episode_timeout = None
        self.steps_counter = None
        self.action_mapper = None
        self.reward_mode = None
        self.aggregate_reward = 0
        self.must_finish_length = 0
        self.previous_reward = 1
        self.state_mode = None

    def step(self, action):
        # print(action)
        if isinstance(self.action_space, spaces.Discrete):
            action_name = self.action_mapper[action]
            l = self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)
            action_options = [x for x in l if x.name == action_name]
            if len(action_options) == 0:
                # reward = self._reward()
                reward = -1
                self.steps_counter += 1
                return self.last_state, reward, True, False, {}
            else:
                action = action_options[0]

        self.bprogram.advance_bthreads(self.bprogram.tickets, action)
        reward = self._reward()
        new_state = self.state_to_gym_space(False)
        self.steps_counter += 1
        bprogram_done = self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets).__len__() == 0
        try:
            # bprogram_done = bprogram_done or self.steps_counter == self.episode_timeout
            bprogram_done = bprogram_done or self.steps_counter == self.episode_timeout or (
                        self.last_state == new_state).all() #or reward > 0
        except Exception:
            bprogram_done = bprogram_done or self.steps_counter == self.episode_timeout
        self.last_state = new_state
        # print(new_state)
        return new_state, reward, bprogram_done, False, {}

    def reset(self, seed=None):
        self.steps_counter = 0
        self.aggregate_reward = 0
        self.must_finish_length = 0
        self.previous_reward = 1
        self.last_event = None
        self.bprogram = self.bprogram_generator()
        self.action_space.bprogram = self.bprogram
        self.bprogram.setup()
        state = self.state_to_gym_space(True)
        self.hot_states = [False] * len(self.bprogram.tickets)
        self.last_state = state
        # print(state)
        return state, None

    def render(self, mode='human', close=False):
        raise NotImplementedError

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def set_bprogram_generator(self, bprogram_generator):
        self.bprogram_generator = bprogram_generator

    def must_finish(self):
        return [x.get('mustFinish', False) for x in self.bprogram.tickets]

    def state_to_gym_space(self, initial):
        bt_states = [str(x.get('state')) for x in self.bprogram.tickets if 'state' in x]
        if initial:
            bt_states.append("1")
        else:
            bt_states.append("0")
        a = np.array("_".join(bt_states).split("_")).astype(np.float32)
        if self.reward_mode == "a":
            a = np.append(a,self.must_finish_length)
        if self.state_mode == "r":
            a[1] = a[0] - a[1]
            return a[1:]
        elif self.state_mode == "ar":
            return np.append(a,a[0]-a[1])
        elif self.state_mode == "a":
            return a

    def _reward(self):
        if self.reward_mode == "r":
            reward = 0
            new_hot_states = self.must_finish()
            for j in range(len(self.hot_states)):
                if self.hot_states[j] and not new_hot_states[j]:
                    reward += 1
                if not self.hot_states[j] and new_hot_states[j]:
                    reward += -1
            self.hot_states = new_hot_states
            # if reward == 0 and any(new_hot_states):
            #     reward = -0.001
            return reward
        elif self.reward_mode == "a":
            # valid only for single must finish
            reward = 0
            new_hot_states = self.must_finish()
            for j in range(len(self.hot_states)):
                if self.hot_states[j] and not new_hot_states[j]:
                    a = self.aggregate_reward
                    self.aggregate_reward = 0
                    self.previous_reward = 1
                    self.must_finish_length = 0
                    return a
                if new_hot_states[j]:
                    reward += -(self.previous_reward/2)
                    self.aggregate_reward += self.previous_reward/2
                    self.must_finish_length += 1
                    self.previous_reward = self.previous_reward/2
            self.hot_states = new_hot_states
            return reward



    def replace_if_disabled(self, action):
        action_name = self.action_mapper[action]
        l = self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)
        action_options = [x for x in l if x.name == action_name]
        if len(action_options) == 0:
            possible_keys = []
            for n in l:
                possible_keys.append([k for k, v in self.action_mapper.items() if n.name == v][0])
            return random.choice(possible_keys)
        else:
            return action

    def close(self):
        super().close()
        self.bprogram = None
        self.action_space.bprogram = None
