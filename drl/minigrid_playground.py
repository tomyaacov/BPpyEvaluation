import minigrid
from minigrid.wrappers import ImgObsWrapper
import gymnasium as gym


# env = gym.make("MiniGrid-Empty-5x5-v0", render_mode="human")
# observation, info = env.reset(seed=42)
# for _ in range(1000):
#    action = env.action_space.sample()
#    observation, reward, terminated, truncated, info = env.step(action)
#
#    if terminated or truncated:
#       observation, info = env.reset()
# env.close()


env = gym.make("MiniGrid-DoorKey-5x5-v0", render_mode="human")

observation, info = env.reset(seed=42)

print(observation)
for _ in range(10000):
   action = env.action_space.sample()
   observation, reward, terminated, truncated, info = env.step(action)
   print(reward)
   if terminated or truncated:
      observation, info = env.reset()
env.close()

