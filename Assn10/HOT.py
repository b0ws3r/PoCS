import math
import random
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from IPython import display
from time import sleep

from scipy import ndimage


def p_fire(i,j):
    global l, norm_denom
    return (math.e**(-i/l) * math.e**(-j/l))


def run_percolation(world):
    N1 = world.shape[0]
    N2 = world.shape[1]
    for i in range(N1):  # for cell in every row
        for j in range(N2):  # and every column
            probability = p_fire(i, j)
            die = random.uniform(0, 1)
            if die < probability:
                world[(i, j)] = 1
            else:
                world[(i, j)] = 0
    return world


def get_spot_with_max_yield_for_d(forest, spark, d, yields_list):
    forest_yields = np.zeros((L,L))
    for _ in range(d):
        test_forest = forest.copy()
        forest_structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]  # define connection
        # pick a random unpopulated spot and add a tree in the forest
        empty_spots = np.argwhere(test_forest == 0)
        test_tree = random.choice(empty_spots)
        test_forest[test_tree[0], test_tree[1]] = 1
        # now calculate the cluster size given that test tree at that spot
        labeled_forest, nb_labels = ndimage.label(test_forest, forest_structure)  # label clusters
        fire_prob = p_fire(test_tree[0], test_tree[1])
        cluster_size = labeled_forest[test_tree[0], test_tree[1]]
        forest_yield = fire_prob * cluster_size

        forest_yields[test_tree[0], test_tree[1]] = forest_yield
        # we want d, forest yield, and density(meaning spark)
        yields_list.append([d, forest_yield, p_fire(test_tree[0], test_tree[1])])
    # out of d choices, which spot had the highest yield?
    ideal_spot = np.unravel_index(forest_yields.argmax(), forest_yields.shape)
    return ideal_spot


L = 64  # height, width
l = L / 10
ds = [10,20,int(L/2), L]
# get norm constant
norm_denom = 0
for i in range(L):
    for j in range(L):
        norm_denom += (math.e**(-i/l) * math.e**(-j/l))

for d in ds:
    # initial conditions of zero
    spark_dist = np.zeros((L, L))
    spark_dist = run_percolation(spark_dist)
    forest = np.zeros((L, L))
    yields_list = list() # some empty spaces here prob.
    for i in range(L):
        for j in range(L):
            spot = get_spot_with_max_yield_for_d(forest, spark_dist, 4, yields_list)
            forest[spot[0], spot[1]] = 1

    # plots
    # plt.imshow(forest, cmap=plt.get_cmap(cm.bone), origin='lower')
    # plt.savefig(f'Plots/{d}')
    #
    df = pd.DataFrame(yields_list, columns=["d", "yield", "density"])
    plt.scatter(df['density'], df['yield'])
    plt.savefig(f'Plots/yields_{d}')
    plt.clf()

