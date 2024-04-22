import numpy as np

for n in range(6, 31):
  content = np.loadtxt('sampling/dice_{}.csv'.format(n),skiprows=1, delimiter=',',)
  top_sec = content[:500:3]
  middle_sec = content[500:2000:10]
  bottom_sec = content[2000::100]
  short = np.concatenate([top_sec, middle_sec, bottom_sec])
  np.savetxt('sampling/mini_dice_{}.csv'.format(n),short, delimiter=',',comments='',header='mean, sem, time, max_sem, min_sem')
  
