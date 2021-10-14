import matplotlib
import pandas as pd
from Monktools import statstools, plottools
matplotlib.use('Agg')
import numpy as np


def power_law(k_min, k_max, y, gamma):
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))


a, xmin = 2.5, 1.0
N = 10000

nodes = 1000
scale_free_distribution = np.zeros(nodes, float)
k_min = 1.0
k_max = 100*k_min
gamma = 2.5
for n in range(nodes):
    scale_free_distribution[n] = power_law(k_min, k_max, np.random.uniform(0,1), gamma)

for i in range(nodes):
    scale_free_distribution[i]
# pl.savefig('powerlaw_variates.png')
