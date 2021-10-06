from typing import Union, List, Tuple

from sklearn.linear_model import LinearRegression
import numpy
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import linregress

def get_dataframe(path):
    return pd.read_csv(path)

def get_filter_gt(dataframe, column_to_filter, filter_value):
    data_filter = dataframe[column_to_filter] > filter_value
    filtered_dataset = dataframe[data_filter]
    return filtered_dataset

def get_filter_lt(dataframe, column_to_filter, filter_value):
    data_filter = dataframe[column_to_filter] < filter_value
    filtered_dataset = dataframe[data_filter]
    return filtered_dataset

def get_filter_eq(dataframe, column_to_filter, filter_value):
    data_filter = dataframe[column_to_filter] == filter_value
    filtered_dataset = dataframe[data_filter]
    return filtered_dataset

def get_filter_in(dataframe, column_to_filter, filter_value):
    data_filter = dataframe[column_to_filter].isin(filter_value)
    filtered_dataset = dataframe[data_filter]
    return filtered_dataset

def get_logs_2axes(dataframe, xvalue, yvalue):
    X = dataframe[xvalue].values  # values converts it into a numpy array
    Y = dataframe[yvalue].values
    FX = numpy.zeros(len(X))
    FY = numpy.zeros(len(Y))
    for idx, x in enumerate(X):
        if float(x) > 0: FX[idx] = numpy.log10(float(x))
        else: FX[idx] = 0;
    for idx, y in enumerate(Y):
        if float(y) > 0:
            FY[idx] = numpy.log10(float(y))
        else:
            FY[idx] = 0

    FX2 =FX.tolist()
    FY2 =FY.tolist()
    dataframe[xvalue + "_log"] = FX2
    dataframe[yvalue + "_log"] = FY2
    return dataframe


def get_logs_1axis(dataframe, col):
    X = dataframe[col].values  # values converts it into a numpy array
    FX = numpy.zeros(len(X))
    for idx, x in enumerate(X):
        if float(x) > 0: FX[idx] = numpy.log10(float(x))
        else: FX[idx] = 0;
    FX2 =FX.tolist()
    dataframe[col + "_log"] = FX2
    return dataframe


def get_linear_regression(dataset, x, y):
    X = dataset[x].values.reshape(-1, 1)
    Y = dataset[y].values.reshape(-1, 1)
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions
    return Y_pred, linear_regressor.intercept_, linear_regressor.coef_


def get_normalized_records(dataframe, coef, untranformed_intercept):
    intercept = 10 ** (untranformed_intercept)
    arr = numpy.zeros(len(dataframe['Record']))
    for idx in range(0, len(dataframe['Record'] - 1)):
        arr[idx] = 100 * ((dataframe['Record'].values[idx] / (intercept * dataframe['Weight'].values[idx] ** coef)) - 1)
    return arr


def get_max_from_normalized(dataframe):
    dataFilter = dataframe['Normalized'] == numpy.amax(dataframe['Normalized'].values)
    return dataframe[dataFilter]


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

def plot_fit(ax: plt.Axes,
             x_vals: List[Union[int, float, np.float64]],
             y_vals: List[Union[int, float, np.float64]],
             low_fit: Union[None, int, float, np.float64] = None,
             high_fit: Union[None, int, float, np.float64] = None,
             color: str = 'C0'):
    """
    Plots a fitted line to the matplotlib Axes object passed to it.
    :param ax: matplotlib axes object to plot to.
    :param x_vals: List of numeric data types. Can also take an numpy
    ndarray, although type checking will complain. The independent values.
    :param y_vals: List of numeric data types. Can also take an numpy
    ndarray, although type checking will complain. The dependent values.
    :param low_fit: Minimum end of range to fit regression line to. All data
    points associated with values in x_values less than or equal to
    this value will be excluded from the fit. If no value is passed no data
    will be trimmed from the lower end of the data.
    :param high_fit: Maximum end of range to fit regression line to. All data
    points associated with values in x_values greater than or equal to
    this value will be excluded from the fit. If no value is passed no data
    will be trimmed from the upper end of the data.
    :param color: color of line to plot. Any string accepted by matplotlib
    may be used.
    :return: Returns the parameters of the fit.
    """
    # Validate x_vals, y_vals input
    if len(x_vals) != len(y_vals):
        raise ValueError("x_vals and y_vals must be equal in length")
    if len(x_vals) < 2:
        raise ValueError("We can't fit a line to data consisting of less than "
                         "two values.")
    # Set low and high cutoffs to minimum and maximum of range if not defined.
    if low_fit is None:
        low_fit = np.array([min(x_vals)])
        low_fit = np.nan_to_num(low_fit)[0]
    if high_fit is None:
        high_fit = np.array([max(x_vals)])
        high_fit = np.nan_to_num(high_fit)[0]
    # Trim data outside of range:
    trimmed_x_vals = np.array([x for x in x_vals
                               if low_fit <= x <= high_fit])
    trimmed_y_vals = np.array([y for x, y in zip(x_vals, y_vals)
                               if low_fit <= x <= high_fit])
    trimmed_x_vals = np.nan_to_num(trimmed_x_vals)
    trimmed_y_vals = np.nan_to_num(trimmed_y_vals)
    # Fit line and plot
    slope, intercept, r, p, stderr = linregress(trimmed_x_vals, trimmed_y_vals)
    fit_x_vals = [min(trimmed_x_vals), max(trimmed_x_vals)]
    fit_y_vals = [x * slope + intercept for x in fit_x_vals]
    ax.plot(fit_x_vals, fit_y_vals,
            label=f"({fit_x_vals[0]:0.2f}, {fit_x_vals[1]:0.2f}), "
                  f"m={slope:0.2f}, b={intercept:0.2f}",
            color=color)
    return slope, intercept, r, p, stderr