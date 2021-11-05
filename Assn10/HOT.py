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


def calculate_spark_distribution(world):
    N1 = world.shape[0]
    N2 = world.shape[1]
    for i in range(N1):  # for cell in every row
        for j in range(N2):  # and every column
            world[(i, j)] = p_fire(i, j)
    return world


def get_spot_with_max_yield_for_d(forest, spark, d):
    test_forests = []
    yields = []
    empty_spots = np.argwhere(forest == 0)

    for _ in range(d):
        test_forest = forest.copy()
        # pick a random unpopulated spot and add a tree in the forest
        test_tree = random.choice(empty_spots)
        test_forest[test_tree[0], test_tree[1]] = 1
        # now calculate the cluster size given that test tree at that spot
        # yield of forest for this spot
        test_forest_yield = get_yield(test_forest, spark)
        # test_forests = np.r_[test_forests, test_forest]
        yields.append(test_forest_yield)
        test_forests.append(test_forest)
        # we want d, forest yield, and density(meaning spark)
        # yields_list.append([d, test_forest_yield, p_fire(test_tree[0], test_tree[1])])

    # out of d choices, which spot had the highest yield?
    index_of_winner = np.array(yields).argmax()
    return test_forests[index_of_winner], yields[index_of_winner]


def get_yield(forest, spark):
    labeled_forest, nb_labels = ndimage.measurements.label(forest)  # label clusters
    trees_in_forest = forest.cumsum()[-1]
    cost = 0

    # todo: labeled forest needs to have size of cluster at each index
    for i in range(L):
        for j in range(L):
            if(labeled_forest[i, j] >0):
                cluster_size = len(np.where(labeled_forest == labeled_forest[i, j])[0])
                cost = cost + cluster_size * spark[i, j]
    forest_yield = (float(trees_in_forest) - cost)/(L*L*1.00)

    return forest_yield

L = 32  # height, width
l = L / 10
ds = [2,20,int(L/2), L]
# get norm constant
norm_denom = 0
for i in range(L):
    for j in range(L):
        norm_denom += (math.e**(-i/l) * math.e**(-j/l))


# initial conditions of zero
spark_dist = np.zeros((L, L))
spark_dist = calculate_spark_distribution(spark_dist)
for d in ds:
    forest = np.zeros((L, L))
    yields_list = list() # this is to track the yield of the chosen spot for each d
    max_yield = 0 # this is to keep watch for an optimal matrix
    forest_with_max_yield = np.zeros((L,L)) # this is the matrix having max_yield

    for i in range(L*L):
        forest, forest_yield = get_spot_with_max_yield_for_d(forest, spark_dist, d)
        yields_list.append([d, forest_yield, forest.cumsum()[-1]/(L*L*1.00)])
        # this forest is pretty cool, set it as the maximum
        if forest_yield > max_yield:
            max_yield = forest_yield
            forest_with_max_yield = forest

    # plots
    plt.imshow(forest_with_max_yield, cmap=plt.get_cmap(cm.bone), origin='lower')
    plt.savefig(f'Plots/max_yield_forest_for_designparam_{d}')

    # TODO plot max yield as function of density
    df = pd.DataFrame(yields_list, columns=["d", "yield", "density"])
    # plt.scatter(df['density'], df['yield'])
    # plt.savefig(f'Plots/yields_{d}')
    plt.clf()

