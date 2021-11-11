import math
import random
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from time import sleep

from scipy import ndimage

from Monktools import ranktools, plottools


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

    for i in range(L):
        for j in range(L):
            if(labeled_forest[i, j] >0):
                cluster_size = len(np.where(labeled_forest == labeled_forest[i, j])[0])
                cost = cost + cluster_size * spark[i, j]
    forest_yield = (float(trees_in_forest) - cost)/(L*L*1.00)

    return forest_yield


def get_and_plot_cluster_size_zipf(ax,cluster_sizes, d, max_yield, density):
    df = pd.DataFrame(cluster_sizes, columns=["size"])
    dist = ranktools.group_data(df, "size", "n_k")
    p_str = str(round(density,2)).replace(".","-")
    y_str = str(round(max_yield,2)).replace(".","-")
    x_vals, log_nk = ranktools.plot_zipf(ax, list(df['size']), 'C0', f"Zipf for cluster dist: D={d}")
    slope_new, intercept_new, r_new, p_new, stderr_new = plottools.plot_fit(ax, x_vals, log_nk)
    # fig2.show(ax)


def get_and_plot_cluster_size_zipf_special(ax,cluster_sizes, density, color):
    df = pd.DataFrame(cluster_sizes, columns=["size"])
    dist = ranktools.group_data(df, "size", "n_k")
    x_vals, log_nk = ranktools.plot_zipf(ax, list(dist['n_k']), color=color, label=f'density: {str(density)}')
    slope_new, intercept_new, r_new, p_new, stderr_new = plottools.plot_fit(ax, x_vals, log_nk, color=color)

    # fig2.show(ax)


L = 32  # height, width
l = L / 10
ds = [1, 2, int(L), int(L**2)]
ds = [int(L**2)]
# ds = [1, 2, 3]
# get norm constant
norm_denom = 0
for i in range(L):
    for j in range(L):
        norm_denom += (math.e**(-i/l) * math.e**(-j/l))

spark_dist = np.zeros((L, L))
spark_dist = calculate_spark_distribution(spark_dist)

def first_parts():
    # initial conditions of zero
    fig1, axz = plt.subplots()
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
        ax1.set_title(f"Optimal forest for D={d} and L={L}")
        ax1.imshow(forest_with_max_yield, cmap=plt.get_cmap(cm.bone), origin='lower')

        # yield curves
        df = pd.DataFrame(yields_list, columns=["d", "yield", "density"])

        p_str = str(round(max_density, 2)).replace(".", "-")
        y_str = str(round(max_yield, 2)).replace(".", "-")
        axz.plot(df['density'], df['yield'], label=f'D={d}, peak yield at({str(round(max_density, 2))},{str(round(max_yield, 2))})')

        p_str = str(round(max_density, 2)).replace(".", "-")
        y_str = str(round(max_yield, 2)).replace(".", "-")
        print(f"Yield curve D={d} - peak yield at ({p_str},{y_str})")

        # zipf
        structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]  # define connection
        labeled_forest, nb_labels = ndimage.label(forest_with_max_yield, structure)  # label clusters
        cluster_sizes_at_peak_yield = ndimage.sum(forest_with_max_yield, labeled_forest, range(nb_labels + 1))
        filter = cluster_sizes_at_peak_yield > 0

        cluster_sizes_at_peak_yield_f = cluster_sizes_at_peak_yield[filter]

        get_and_plot_cluster_size_zipf(ax2, cluster_sizes_at_peak_yield_f, d, max_yield, max_density)
        ax2.legend()
        ax2.set_title(f'Zipf distribution for dimension {d}')
        fig.savefig(f'Plots/forest_plots_dim_{d}')
        plt.clf()

    axz.legend()
    axz.set_xlabel('Forest Density')
    axz.set_ylabel('Yield')
    fig1.savefig(f'Plots/yield_curves')


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def last_part():
# lastly
    cmap = get_cmap(9)
    forest = np.zeros((L, L))
    figd, axz = plt.subplots()
    for i in range(L * L):
        forest, forest_yield, density = get_spot_with_max_yield_for_d(forest, spark_dist, L**2)
        labeled_forest, nb_labels = ndimage.measurements.label(forest)  # label clusters
        cluster_sizes = ndimage.sum(forest, labeled_forest, range(nb_labels + 1))
        filter = cluster_sizes > 0
        nonzero_cluster_sizes = cluster_sizes[filter]

        done = 0
        if (i == math.floor(L*L/10.0)) & done == 0:
            print(round(density,2))
            get_and_plot_cluster_size_zipf_special(axz, nonzero_cluster_sizes, density, cmap(0))
            done += 1
        if (i == math.floor(1* L*L/10.0))& done == 1:
            get_and_plot_cluster_size_zipf_special(axz, nonzero_cluster_sizes, density, cmap(1))
            done += 1
        if (i == math.floor(3* L*L/10.0))& done == 2:
            get_and_plot_cluster_size_zipf_special(axz, nonzero_cluster_sizes, density, cmap(2))
            done += 1
        if (i == math.floor(4 * L*L/10.0))& done == 3:
            get_and_plot_cluster_size_zipf_special(axz, nonzero_cluster_sizes, density, cmap(3))
            done += 1
        if (i == math.floor(5* L*L/10.0))& done == 4:
            get_and_plot_cluster_size_zipf_special(axz, nonzero_cluster_sizes, density, cmap(4))
            done += 1
        if (i == math.floor(6 * L*L/10.0))& done == 5:
            get_and_plot_cluster_size_zipf_special(axz, nonzero_cluster_sizes, density, cmap(5))
            done += 1
        if (i == math.floor(7* L*L/10.0))& done == 6:
            get_and_plot_cluster_size_zipf_special(axz, nonzero_cluster_sizes, density, cmap(6))
            done += 1
        if (i == math.floor(8*L*L/10.0)) & done == 7:
            get_and_plot_cluster_size_zipf_special(axz, nonzero_cluster_sizes, density, cmap(7))
            done += 1
        if (i == math.floor(9*L*L/10.0))& done == 8:
            get_and_plot_cluster_size_zipf_special(axz, nonzero_cluster_sizes, density, cmap(8))
            break

    axz.legend()
    axz.set_title("Cluster size for varying densities")
    figd.savefig(f"Plots/cluster_size_zipf_L2.png")


# first_parts()
last_part()