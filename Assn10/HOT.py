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

from Monktools import ranktools


def run_percolation(world, probability, l):
    for i in range(l):  # for cell in every row
        for j in range(l):  # and every column
            die = random.uniform(0, 1)
            if die < probability:
                world[(i, j)] = 1
            else:
                world[(i, j)] = 0

    return world


def p_fire(i,j):
    global l, norm_denom
    return (math.e**(-i/l) * math.e**(-j/l))/norm_denom


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
    densities = []
    empty_spots = np.argwhere(forest == 0)

    for _ in range(d):
        test_forest = forest.copy()
        # pick a random unpopulated spot and add a tree in the forest
        test_tree = random.choice(empty_spots)
        test_forest[test_tree[0], test_tree[1]] = 1
        # now calculate the cluster size given that test tree at that spot
        # yield of forest for this spot
        test_forest_yield = get_yield(test_forest, spark)
        yields.append(test_forest_yield)
        test_forests.append(test_forest)
        densities.append(forest.cumsum()[-1]/(L*L*1.00))

    # out of d choices, which spot had the highest yield?
    index_of_winner = np.array(yields).argmax()
    return test_forests[index_of_winner], yields[index_of_winner], densities[index_of_winner]


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


def get_and_plot_cluster_size_zipf(cluster_sizes, d, max_yield, density):
    df = pd.DataFrame(cluster_sizes, columns=["size"])
    dist = ranktools.group_data(df, "size", "n_k")
    fig2, ax = plt.subplots()
    p_str = str(round(density,2)).replace(".","-")
    y_str = str(round(max_yield,2)).replace(".","-")
    x_vals, log_nk = ranktools.plot_zipf(ax, list(dist['n_k']), 'C0', f"Yield curve D={d} - peak yield at ({p_str},{p_str})")
    # fig2.show(ax)
    fig2.savefig(f"Plots/cluster_size_zipf_{str(d)}_yield_{y_str}.png")



L = 32  # height, width
l = L / 10
ds = [1, 2, int(L), int(L**2)]
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
    max_density = 0
    if d == 1:
        forest = run_percolation(forest, 0.5, L)
        max_density = (forest.cumsum()[-1]/(L*L*1.00))
        forest_with_max_yield = forest
        max_yield = get_yield(forest_with_max_yield, spark_dist)
    else:
        for i in range(L*L):
            forest, forest_yield, density = get_spot_with_max_yield_for_d(forest, spark_dist, d)
            yields_list.append([d, forest_yield, forest.cumsum()[-1]/(L*L*1.00)])
            # this forest is pretty cool, set it as the maximum
            if forest_yield > max_yield:
                max_yield = forest_yield
                forest_with_max_yield = forest
                max_density = density

    # plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    ax1.imshow(forest_with_max_yield, cmap=plt.get_cmap(cm.bone), origin='lower')

    structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]  # define connection
    labeled_forest, nb_labels = ndimage.label(forest_with_max_yield, structure)  # label clusters
    cluster_sizes_at_peak_yield = ndimage.sum(forest_with_max_yield, labeled_forest, range(nb_labels + 1))
    filter = cluster_sizes_at_peak_yield > 0
    cluster_sizes_at_peak_yield_f = cluster_sizes_at_peak_yield[filter]
    df = pd.DataFrame(yields_list, columns=["d", "yield", "density"])
    ax2.scatter(df['density'], df['yield'])
    fig.savefig(f'Plots/forest_plots_dim_{d}')
    plt.clf()
    get_and_plot_cluster_size_zipf(cluster_sizes_at_peak_yield_f, d, max_yield, max_density)


