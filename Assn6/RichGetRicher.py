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


elephant_groups = [ElephantGroup()]  # initialize with one elephant of random color

# rho close to 0 means a lot of elephants of the same color
# rho close to 1 means a lot of different elephants out there
rho = .1

# maximum steps to run simulation
t_max = 27


def perform_innovation():
    p = random.uniform(0, 1)
    if p < rho:
        return True
    else:
        return False


def zipf(dataframe, yvalue, title):
    dataframe['rank'] = dataframe[yvalue].rank(ascending=False)
    loggified_df = statstools.get_logs_1axis(dataframe, 'rank')
    plottools.plot_results(loggified_df, 'rank_log', yvalue + '_log', 'Zipf plot for' + title)
    return loggified_df


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


for rc in [.1, 0.01, 0.001]:
    elephant_groups = [ElephantGroup()]
    rho = rc

    runs = []
    for i in range(t_max):
        replicate_elephants()
        print(i)
    runs.append(elephant_groups.copy())
    print(f"Number of groups of elephants: {len(elephant_groups)}")

    size_1_elephant_groups = list(filter(lambda group: group.size == 1, elephant_groups))
    print(f"Number of groups of elephants of size 1: {len(size_1_elephant_groups)}")

    # get list of elephant group sizes
    groups_of_size_k = list(map(lambda g: g.size, elephant_groups))
    groups_of_size_k = list(filter(lambda g: g > 0 , groups_of_size_k))
    raw = pd.DataFrame(groups_of_size_k, columns=['k'])
    n_k = raw['k'].value_counts(sort=True)
    n_k = n_k.rename_axis('k').reset_index(name='N')

    # get zipf and return data
    fig, ax = plt.subplots()
    x_vals, log_nk = statstools.plot_zipf(ax, list(n_k['N']), 'C0', 'Elephants')

    # plot the fit and get the slope back
    slope, intercept, r, p, stderr = statstools.plot_fit(ax, x_vals, log_nk, 0, 3, 'lime')
    print(slope)
    plt.savefig(f"Plots/richgetricher_simulation_alpha{slope}_tmax{t_max}_rho{rho}.jpg")
    plt.show()

