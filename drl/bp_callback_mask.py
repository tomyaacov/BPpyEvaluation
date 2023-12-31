from stable_baselines3.common.callbacks import BaseCallback
from sb3_contrib import MaskablePPO
from concurrent.futures import ThreadPoolExecutor
from ttt_helper import get_env, get_bprogram
import tempfile

class BPCallbackMask(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: Verbosity level: 0 for no output, 1 for info messages, 2 for debug messages
    """
    def __init__(self, verbose=0, repeat=1):
        super(BPCallbackMask, self).__init__(verbose)
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
        self.repeat = repeat

    def test(self, model, env, threshold=-0.5):
        if self.repeat > 1:
            def evaluate_single(model):
                temp_dir = tempfile.TemporaryDirectory()
                model.save(temp_dir.name + "/model")
                model = MaskablePPO.load(temp_dir.name + "/model")
                env = get_env()
                observation, _ = env.reset()
                reward_sum = 0
                counter = 0
                values = []
                actions = []
                while True:
                    action_masks = env.action_masks()
                    action, _states = model.predict(observation, deterministic=True, action_masks=action_masks)
                    actions.append(action)
                    observation, reward, done, _,  info = env.step(action.item())
                    reward_sum += reward
                    counter += 1
                    # print(action, observation, reward, done, info)
                    if done:
                        break
                if reward_sum == -2:
                    print(actions)
                return reward_sum
            model.action_space.bprogram = None
            with ThreadPoolExecutor(100) as executor:
                processes = [executor.submit(evaluate_single, model) for _ in range(self.repeat)]
                rewards = [p.result() for p in processes]
            model.action_space.bprogram = get_bprogram()
            if all([r == 0 for r in rewards]):
                self.should_end = True
            print(model.num_timesteps, sum([int(r == 0) for r in rewards]))
            #print(model.num_timesteps, rewards)
        else:
            _env = env.envs[0]
            observation = env.reset()
            reward_sum = 0
            counter = 0
            values = []
            actions = []
            while True:
                action_masks = _env.action_masks()
                action, _states = model.predict(observation, deterministic=True, action_masks=action_masks)
                actions.append(action)
                observation, reward, done, info = env.step(action)
                reward_sum += reward
                counter += 1
                # print(action, observation, reward, done, info)
                if done[0]:
                    break
            # print("optimal reward: ", reward_sum)
            if reward_sum > threshold:
                self.should_end = True



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