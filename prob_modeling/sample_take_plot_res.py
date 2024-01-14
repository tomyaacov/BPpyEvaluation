import numpy as np

def q_params(min_doors=3,max_doors=10):
    combs = []
    for d in range(min_doors, max_doors+1):
        for p in range(1, d):
            for o in range(1, d-p):
                if (p == 1 and d == 9):
                    pass
                elif (o < 6):
                    combs.append((d,p,o))
    return combs
q_params(3, 6)

for params in q_params(3, 10):

  content = np.loadtxt('sampling/sample_{}d{}p{}o.csv'.format(*params),skiprows=1, delimiter=',',)
  top_sec = content[:500:3]
  middle_sec = content[500:2000:10]
  bottom_sec = content[2000::100]
  short = np.concatenate([top_sec, middle_sec, bottom_sec])
  np.savetxt('sampling/short_{}d{}p{}o.csv'.format(*params),short, delimiter=',',comments='',header='mean, sem, time, max_sem, min_sem')
  