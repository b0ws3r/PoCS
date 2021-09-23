from sklearn.linear_model import LinearRegression
import numpy
import pandas as pd


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
