from bppy import *
from bppy.gym import *
from stable_baselines3 import PPO

@b_thread
def control():
    while True:
        yield {waitFor: BEvent("HOT")}
        yield {waitFor: BEvent("COLD"), block: BEvent("HOT")}

@b_thread
def add_cold():
    for i in range(3):
        yield {request: BEvent("COLD")}
@b_thread
def add_hot():
  for i in range(3):
    yield {request:BEvent("HOT"),localReward:-0.1}
  yield {request:BEvent("DONE_HOT"),localReward:1}

def init_bprogram():
  ess=SimpleEventSelectionStrategy()
  return BProgram(bthreads=[add_hot(),add_cold(),
                            control()],
                  event_selection_strategy=ess)

reward_fun=lambda rewards: sum(filter(None,rewards))

env=BPEnv(bprogram_generator=init_bprogram,
          action_list=[BEvent("HOT"),BEvent("COLD"),
                       BEvent("DONE_HOT")],
          observation_space=SimpleBPObservationSpace(init_bprogram, [BEvent("HOT"),BEvent("COLD"), BEvent("DONE_HOT")]),
          reward_function=reward_fun)

model=PPO("MlpPolicy",env,verbose=1)
model.learn(total_timesteps=100000)


class ModelBasedStrategy(SimpleEventSelectionStrategy):

  def __init__(self, model, env):
    self.model=model
    self.env=env

  def select(self, statements, external_events_queue=[]):
    s=self.env._state()
    action,_=self.model.predict(s)
    event=self.env.action_space.event_list[action]
    if event in self.selectable_events(statements):
      return event
    else:
      # If the model selects a disabled event,
      # use the previous strategy
      return super().select(statements)

def init_bprogram_eval(model,env):
  ess=ModelBasedStrategy(model,env)
  return BProgram(bthreads=[add_hot(),add_cold(),
                            control()],
                  event_selection_strategy=ess,
                  listener=PrintBProgramRunnerListener())

bprogram_gen=lambda:init_bprogram_eval(model,env)
env.bprogram_generator=bprogram_gen
env.reset()
env.bprogram_generator().run()