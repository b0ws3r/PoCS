from sklearn.linear_model import LinearRegression
import numpy

class STATS:
    def get_filter(self, dataframe, column_to_filter, filter_value):
        data_filter = dataframe[column_to_filter] == filter_value
        filtered_dataset = dataframe[data_filter]
        return filtered_dataset

    def get_linear_regression(self, dataset, x, y, use_log):
        X = dataset[x].values  # values converts it into a numpy array
        Y = dataset[y].values
        if use_log:
            FX = numpy.zeros(len(X))
            FY = numpy.zeros(len(Y))
            for idx, x in enumerate(X):
                FX[idx] = numpy.log10(float(x))
            for idx, y in enumerate(Y):
                FY[idx] = numpy.log10(y)
            FX2 = numpy.reshape(FX, (len(X), 1))
            FY2 = numpy.reshape(FY, (len(Y), 1))
        else:
            FX2 = X.reshape(-1, 1)
            FY2 = Y.reshape(-1, 1)

        linear_regressor = LinearRegression()  # create object for the class
        linear_regressor.fit(FX2, FY2)  # perform linear regression
        Y_pred = linear_regressor.predict(FX2)  # make predictions
        return FX2, FY2, Y_pred, linear_regressor.intercept_, linear_regressor.coef_

    def GetNormalizedRecords(self, dataframe, coef, untranformed_intercept):
        intercept = 10 ** (untranformed_intercept)
        arr = numpy.zeros(len(dataframe['Record']))
        for idx in range(0, len(dataframe['Record'] - 1)):
            arr[idx] = 100 * ((dataframe['Record'].values[idx] / (intercept * dataframe['Weight'].values[idx] ** coef)) - 1)
        return arr

    def GetMaxFromNormalized(self, dataframe):
        dataFilter = dataframe['Normalized'] == numpy.amax(dataframe['Normalized'].values)
        return dataframe[dataFilter]
