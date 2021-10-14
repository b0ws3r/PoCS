import numpy
from scipy.stats import powerlaw

import matplotlib.pyplot as plt


# Can do displacement after n steps as a power law dist.
gamma = 5/2
a = gamma + 1


def sample_dist(dist):


    pass


for N in [10, 10**2, 10**3, 10**4, 10**5, 10**6]:
    r = powerlaw.rvs(a, size=1000)

    # create n sets of samples (s_1, s_2, ..., s_n)
    # samples = []
    maximums = []  # maximums should be tuples - i, k_max_i, where k_max_i is the maximum of set i (s_i)

    # for each set s in samples, determine and record the maximum value of the set
    for i in range(N):
        maximums[i] = numpy.max(r)
    # plot i, k_max_i
