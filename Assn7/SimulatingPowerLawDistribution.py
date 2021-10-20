import matplotlib
from typing import List
import pickle
import numpy

from Monktools import plottools

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np


def q_1_a():
    gamma = 5 / 2
    norm_constant = (gamma - 1) / (1 - 10_000_000 ** -(gamma - 1))

    def p_k(k):
        return k ** (-gamma)

    p_k_vals = [p_k(k) for k in range(1, 10_000_000 + 1)]
    bins = [x / norm_constant for x in p_k_vals]
    cum_bins =numpy.zeros(len(bins))
    total = 0
    for idx, bin in enumerate(bins):
        total += bin
        cum_bins[idx] = total

    def filter_portions(boundary: float):
        if  boundary < cum_bins[0]: return 1
        out = numpy.where(boundary > cum_bins)
        return len(out)
        for idx, bin in enumerate(cum_bins):
            if bin > boundary: # given boundary of .99, we want to see if
                return idx+1
        return len(bins)

    def get_power_law_k_value() -> int:
        boundary = np.random.rand()
        k = filter_portions(boundary)
        return k


    def get_max_values(samples: int, sample_size: int) -> List[int]:
        max_vals = list()
        for _ in range(samples):
            values = list()
            for _ in range(sample_size):
                # calculate number of k steps you need to cross a random boundary
                # do this {sample_size} times
                values.append(get_power_law_k_value())
            # now get the max in this set
            max_vals.append(max(values))
        return max_vals

    samplesize_k_max_values_dict = dict()
    for exp in range(1, 7):
        samplesize_k_max_values_dict[10 ** exp] = list()
    for sample_size in samplesize_k_max_values_dict.keys():
        print(f"sample size: {sample_size}")
        samplesize_k_max_values_dict[sample_size] = get_max_values(1000, sample_size)
    for sample_size in samplesize_k_max_values_dict.keys():
        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.add_subplot()
        ax.scatter(list(range(1000)), samplesize_k_max_values_dict[sample_size], s=1)
        ax.set_title(f"Max Values for Sample Sizes of {sample_size:,}")
        ax.legend()
        fig.show()
        plt.savefig(f"Plots/max_values_{sample_size}.jpg")

    pickle.dump(samplesize_k_max_values_dict, open("save.p", "wb"))


# Part b - plot expected k_max
def q_1_b():
    samplesize_k_max_values_dict = pickle.load(open("save.p", "rb"))
    expected_k_max_values = []
    for sample_size in samplesize_k_max_values_dict.keys():
        expected_k_max = numpy.average(samplesize_k_max_values_dict[sample_size])
        expected_k_max_values.append(expected_k_max)

    fig, ax = plt.subplots()
    slope, intercept, r, p, stderr = plottools.plot_fit(ax, np.log10(list(samplesize_k_max_values_dict.keys()))
                                                        , np.log10(expected_k_max_values))
    plt.legend([f"line with alpha = {slope}", "Log10 of expected k max values for sample sizes N"], shadow=True)
    plt.savefig(f"Plots/expected_k_max_fit.jpg")


q_1_a()
