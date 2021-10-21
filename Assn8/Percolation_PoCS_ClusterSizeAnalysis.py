import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
from scipy import ndimage
from Monktools import plottools, ranktools


def run_percolation(world, probability, l):
    for i in range(l):  # for cell in every row
        for j in range(l):  # and every column
            die = random.uniform(0, 1)
            if die < probability:
                world[(i, j)] = 1
            else:
                world[(i, j)] = 0

    return world


def get_percolation_cluster_avg_size(probability, l):
    # initial conditions of zero
    world = np.zeros((l,l))
    world = run_percolation(world, probability, l)  # run model
    # filter largest cluster
    # Site percolation
    structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]  # define connection
    label_world, nb_labels = ndimage.label(world, structure)  # label clusters
    cluster_sizes = ndimage.sum(world, label_world, range(nb_labels + 1))
    return cluster_sizes.max(), cluster_sizes


# Parameters
def q_4():
    l_vals = [20, 50, 100, 200, 500, 1000]  # square lattice of size L
    # l_vals = [20, 50, 100]  # square lattice of size L
    probabilities = np.linspace(0, 1, 100) # occupation probabilities to test


    for l in l_vals:
        print(f"L = {l}")
        prob_to_max_avg_cluster = []
        for idx, p in enumerate(probabilities):
            max_sum = 0
            for i in range(100):  # run 100 tests for each probability
                max_cluster_size = get_percolation_cluster_avg_size(p, l)[0]
                max_sum += max_cluster_size
            max_avg_cluster_size = max_sum/100
            prob_to_max_avg_cluster.append(max_avg_cluster_size/(l*l))
        plt.plot(probabilities, prob_to_max_avg_cluster, label=f"L = {l}")

    plt.legend()
    plt.savefig(f"Plots/p_vs_s_avg_0_{max(l_vals)}")


def get_and_plot_cluster_size_dist(p, l):
    max_cluster_size, cluster_sizes = get_percolation_cluster_avg_size(p, l)
    df = pd.DataFrame(cluster_sizes, columns=["size"])
    dist = ranktools.group_data(df, "size", "n_k")
    # x axis = forest size
    # y axis = num_clusters
    plt.clf()
    plt.scatter(dist["size"], dist["n_k"])
    plt.show()
    p_str = str(round(p,2)).replace(".","-")
    plt.savefig(f"Plots/cluster_size_dist_probability_{p_str}_L_{l}")


# get the fractional size of largest cluster as a function of p for various space sizes
# q_4()

# q_4 plot distribution of cluster sizes for large L and threshold p
p_threshold = 0.592746
get_and_plot_cluster_size_dist(p_threshold, 500)

# q_5 plot distribution of cluster sizes for large L and p values: [p_c/2, p_c + (1-p_c)/2]
get_and_plot_cluster_size_dist(p_threshold/2, 500)
get_and_plot_cluster_size_dist(p_threshold + (1-p_threshold)/2, 500)

