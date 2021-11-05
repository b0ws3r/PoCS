from typing import Union, List, Tuple

from sklearn.linear_model import LinearRegression
import numpy
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import linregress

from Monktools import statstools


def group_data(dataframe, column, grouping_column_name):
    k_n = dataframe[column].value_counts(sort=True)
    k_n = k_n.rename_axis(column).reset_index(name=grouping_column_name)
    return k_n


def plot_zipf(ax: plt.Axes,
              nk,
              color: str = 'C0',
              label: str = ''):
    """
    Plots the zipf distribution of a set of data as a log-log plot.
    :param ax: A matplotlib Axes object.
    :param nk: For a zipf distribution, the number of occurrences of items in a
    dataset.
    :param label: A label for the data. Will be used by matplotlib's legend
    method.
    :param color:
    :return:
    """
    # Make sure the data is sorted.
    nk.sort(reverse=True)
    # Create some x_vals to plot against
    x_vals = np.arange(1, len(nk)+1)
    # Then take the logs of both
    log_nk = np.log10(np.array(nk))
    x_vals = np.log10(x_vals)
    # Then plot
    ax.set_xlabel("N")
    ax.set_ylabel("k")
    ax.set_title(label)
    ax.scatter(x_vals, log_nk, label=label, s=1, color=color)
    # Then return the lists we plotted, in case someone wants to fit a line
    return x_vals, log_nk


def plot_zipf_ccdf(ax: plt.Axes,
                   nk,
                   color: str = 'C0',
                   label: str = ''):
    """
    Plots the zipf ccdf of a set of data as a log-log plot.
    :param ax: A matplotlib Axes object.
    :param nk: For a zipf distribution, the number of occurrences of items in a
    dataset.
    :param label: A label for the data. Will be used by matplotlib's legend
    method.
    :param color:
    :return:
    """
    # Make sure the data is sorted.
    nk.sort(reverse=True)
    # We need to normalize Nk - converting occurrences to probabilities - to
    # get our pdf, from which we can get our cdf, from which we can get our
    # ccdf.
    nk = np.array(nk)
    sum_nk = sum(nk)
    p_nk = nk / sum_nk
    cdf_nk = np.cumsum(p_nk)
    ccdf_nk = 1 - cdf_nk
    # Create some x_vals to plot against
    x_vals = np.array(range(len(nk)))
    # Then take the logs of values
    log_ccdf_nk = list(np.log10(ccdf_nk))
    x_vals = np.log10(x_vals)
    # Then plot
    ax.scatter(x_vals, log_ccdf_nk, label=label, s=1, color=color)
    # Then return the lists we plotted, in case someone wants to fit a line
    return x_vals, log_ccdf_nk


# rho_est = (# of unique words)/(# of all words)
def get_simon_rho_estimate(n_k):
    num_unique_words = n_k['N'].sum()
    total_words = sum(list(n_k['N'] * n_k['k']))
    rho_est = num_unique_words / total_words
    print(f"ESTIMATE OF RHO FROM COUNTS: {rho_est}")
    return rho_est


# number of groups of size n
def get_fraction_of_groups_of_size_n(dataframe, n):
    num_groups = sum(dataframe['N'])  # number of groups total
    num_groups_size_n = statstools.get_filter_eq(dataframe, 'k', n).iloc[-1]['N']  # number of size n
    return num_groups_size_n/num_groups


def n_1(rho):
    return 1 / (2 - rho)


def n_2(rho):
    return (1-rho)/(1+2*(1-rho)) * n_1(rho)


def n_3(rho):
    term1 = 2*(1-rho)/(1+3*(1-rho))
    term2 = n_2(rho)
    return term1 * term2