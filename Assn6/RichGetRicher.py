import random

import matplotlib.pyplot as plt
import pandas as pd

from Monktools import statstools, plottools


class ElephantGroup:
    def __init__(self):
        self.color = innovate()
        self.size = 1


def innovate():
    levels = range(32, 256, 32)
    return tuple(random.choice(levels) for _ in range(3))


# We will see how many different types of elephants reproduce w/ diff colors


elephant_groups = [ElephantGroup()]  # initialize with one elephant of random color

# rho close to 0 means a lot of elephants of the same color
# rho close to 1 means a lot of different elephants out there
rho = .1

# maximum steps to run simulation
t_max = 20


def perform_innovation():
    p = random.uniform(0, 1)
    if p < rho:
        return True
    else:
        return False


def replicate_elephants():
    iterab = elephant_groups.copy()
    for elephant_group in iterab:
        for elephant in range(elephant_group.size):
            if perform_innovation():
                elephant_group.size -= 1
                elephant_groups.append(ElephantGroup())
                # print("innovating")
            else:
                elephant_group.size += 1


for i in range(t_max):
    replicate_elephants()
    print(i)

print(f"Number of groups of elephants: {len(elephant_groups)}")

size_1_elephant_groups = list(filter(lambda group: group.size == 1, elephant_groups))
print(f"Number of groups of elephants of size 1: {len(size_1_elephant_groups)}")

# get list of elephant group sizes
groups_of_size_k = list(map(lambda g: g.size, elephant_groups))
groups_of_size_k = list(filter(lambda g: g > 0 , groups_of_size_k))
raw = pd.DataFrame(groups_of_size_k, columns=['k'])
n_k = raw['k'].value_counts(sort=True)
n_k = n_k.rename_axis('k').reset_index(name='N')
statstools.get_logs_1axis(n_k, 'k')
zipf(n_k, 'k', 'elephants')

fig, ax = plt.subplots()
statstools.plot_zipf(ax, list(n_k['N']), 'C0', 'Elephants')

plt.show()

