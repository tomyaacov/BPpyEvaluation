from gymnasium.spaces import Discrete
import numpy as np


class BPActionSpace(Discrete):

    def __init__(self, action_mapper):
        self.action_mapper = action_mapper
        self.bprogram = None
        Discrete.__init__(self, len(action_mapper))

    def sample(self):
        return self.np_random.choice(self._possible_actions())

    def contains(self, x):
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (x.dtype.char in np.typecodes['AllInteger'] and x.shape == ()):
            as_int = int(x)
        else:
            return False
        return as_int in self._possible_actions()

    def __repr__(self):
        return "BPActionSpace(%d)" % self.n

    def __eq__(self, other):
        return isinstance(other, BPActionSpace) and self.bprogram == other.bprogram and self.action_mapper == other.action_mapper

    def _possible_actions(self):
        possible_events = self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)
        possible_events = [x.name for x in possible_events]
        return [k for k, v in self.action_mapper.items() if v in possible_events]

    def possible_actions(self):
        return self._possible_actions()