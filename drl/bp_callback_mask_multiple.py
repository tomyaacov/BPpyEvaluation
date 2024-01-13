from stable_baselines3.common.callbacks import BaseCallback
import random
from bppy.model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy
import time
import numpy as np
from stable_baselines3 import DQN
from sb3_contrib import QRDQN

class BPCallbackMaskMultiple(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: Verbosity level: 0 for no output, 1 for info messages, 2 for debug messages
    """

    def __init__(self, verbose=0, traces=None, check_every=None):
        super(BPCallbackMaskMultiple, self).__init__(verbose)
        # Those variables will be accessible in the callback
        # (they are defined in the base class)
        # The RL model
        # self.model = None  # type: BaseAlgorithm
        # An alias for self.model.get_env(), the environment used for training
        # self.training_env = None  # type: Union[gym.Env, VecEnv, None]
        # Number of time the callback was called
        # self.n_calls = 0  # type: int
        # self.num_timesteps = 0  # type: int
        # local and global variables
        # self.locals = None  # type: Dict[str, Any]
        # self.globals = None  # type: Dict[str, Any]
        # The logger object, used to report things in the terminal
        # self.logger = None  # stable_baselines3.common.logger
        # # Sometimes, for event callback, it is useful
        # # to have access to the parent object
        # self.parent = None  # type: Optional[BaseCallback]
        self.should_end = False
        self.start_time = time.time()
        self.prob_threshold = 0.001
        self.check_every = check_every
        self.last_check = 0
        self.result = ""
        self.traces = traces

    def test(self, model, env):
        if time.time() - self.start_time - self.last_check < self.check_every:
            return
        traces = self.traces
        results = dict([(x, 0) for x in ["TP", "FP", "TN", "FN"]])
        actions = env.action_space.event_list
        results_traces = []
        for t, l in traces:
            _env = env.envs[0]
            observation = env.reset()
            min_value = 1
            reward_sum = 0
            for e in t:
                if e not in actions:
                    continue
                if isinstance(model, DQN):
                    q_value = model.policy.q_net(model.policy.obs_to_tensor(observation)[0]).detach().cpu().numpy()[0][actions.index(e)]
                else:
                    q_values = model.policy.quantile_net(model.policy.obs_to_tensor(observation)[0]).mean(dim=1)
                    q_value = q_values.detach().cpu().numpy()[0][actions.index(e)]
                min_value = min(min_value, q_value+reward_sum)
                if min_value <= 0:
                    break
                # probs = model.policy.get_distribution(model.policy.obs_to_tensor(observation)[0], action_masks).distribution.probs.detach().numpy()[0]
                # total_prob = min(total_prob, probs[actions.index(e)])
                observation, reward, done, info = env.step(np.array([actions.index(e)]))
                reward_sum += reward.item()
            results_traces.append((min_value, l))
        # print(results_traces)
        # results_traces = sorted(results_traces, key=lambda x: x[0])
        # print(results_traces)
        # p = [x[0] for x in results_traces]
        # print(p)
        # l = [x[1] for x in results_traces]
        # print(l)
        # idx = max(list(range(len(p))), key=lambda i:(len(l[:i])-sum(l[:i])) + sum(l[i:]))
        # print(idx)
        # p_max = (p[idx-1] + p[idx]) / 2
        # print(p_max)
        # print(results_traces)
        for min_value, label in results_traces:
            if label:
                if min_value > 0:
                    results["TP"] += 1
                else:
                    results["FN"] += 1
            else:
                if min_value > 0:
                    results["FP"] += 1
                else:
                    results["TN"] += 1
        self.result += "Time," + str(time.time() - self.start_time) + "," + ",".join([str(k) + "," + str(v) for k,v in results.items()]) + "\n"
        self.last_check = time.time() - self.start_time
        print("Time," + str(time.time() - self.start_time) + "," + ",".join([str(k) + "," + str(v) for k,v in results.items()]))
        if isinstance(model, DQN):
            print(model.policy.q_net(model.policy.obs_to_tensor(np.array([[0,0]]))[0]).detach().cpu().numpy())
        else:
            q_values = model.policy.quantile_net(model.policy.obs_to_tensor(np.array([[0,0]]))[0]).mean(dim=1)
            print(q_values.detach().cpu().numpy())



    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """

    def _on_rollout_start(self) -> None:
        """
        A rollout is the collection of environment interaction
        using the current policy.
        This event is triggered before collecting new samples.
        """
        self.test(self.model, self.training_env)

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: (bool) If the callback returns False, training is aborted early.
        """
        return not self.should_end

    def _on_rollout_end(self) -> None:
        """
        This event is triggered before updating the policy.
        """
        pass

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        pass
