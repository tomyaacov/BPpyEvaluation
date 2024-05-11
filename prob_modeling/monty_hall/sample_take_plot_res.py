import numpy as np
from monty import param_combs


# takes lower resolution of samples
for params in param_combs(3, 10):

  content = np.loadtxt('samples/sample_{}d{}p{}o.csv'.format(*params),skiprows=1, delimiter=',',)
  top_sec = content[:500:3]
  middle_sec = content[500:2000:10]
  bottom_sec = content[2000::100]
  short = np.concatenate([top_sec, middle_sec, bottom_sec])
  np.savetxt('samples/short_{}d{}p{}o.csv'.format(*params),short, delimiter=',',comments='',header='mean, sem, time, max_sem, min_sem')
  