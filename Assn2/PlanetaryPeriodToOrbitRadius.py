import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression
import numpy

def GetLogLinearRegression(dataset, XName, YName):
    X = dataset[XName].values  # values converts it into a numpy array
    Y = dataset[YName].values
    FX = numpy.zeros(len(X))
    FY = numpy.zeros(len(Y))
    for idx, x in enumerate(X):
        FX[idx] = numpy.log10(float(x))
    for idx, y in enumerate(Y):
        FY[idx] = numpy.log10(y)
    FX2 = numpy.reshape(FX, (len(X),1))
    FY2 = numpy.reshape(FY, (len(Y),1))
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(FX2, FY2)  # perform linear regression
    Y_pred = linear_regressor.predict(FX2)  # make predictions
    return FX2, FY2, Y_pred, linear_regressor.intercept_, linear_regressor.coef_

def PlotMultiple(datasAndFits):
    for d in datasAndFits:
        test = d[0]
        plt.scatter(test[0],test[1])
        plt.plot(test[0], test[2], label=d[1])

    plt.legend()
    plt.title('Distance from the sun vs orbital period')
    plt.text(3,3, 'Coefficient: '+ str(datasAndFits[0][0][4]))
    plt.xlabel("log10(Distance from the sun)")
    plt.ylabel("log10(Orbital Period)")
    plt.savefig('Combined' + 'Planets'+'.jpg')
    plt.close()

def GetNormalizedRecords(dataframe, coef, untranformed_intercept):
    intercept = 10 ** (untranformed_intercept)
    arr = numpy.zeros(len(dataframe['Speed']))
    for idx in range(0, len(dataframe['Speed'] - 1)):
        arr[idx] = 100 * ((dataframe['Speed'].values[idx] / (intercept * dataframe['N'].values[idx] ** coef)) - 1)
    return arr

def GetMaxFromNormalized(dataframe):
    dataFilter = dataframe['Normalized'] == numpy.amax(dataframe['Normalized'].values)
    return dataframe[dataFilter]


# Get data from CSV
csvPath = 'Data/PlanetaryOrbitAndDistanceFromSun.csv'
datasAndFits = []

# Planets
dataframe = pd.read_csv(csvPath)
linearFit = GetLogLinearRegression(dataframe, 'DistanceFromSun','OrbitalPeriod')
datasAndFits.append([linearFit,'Planets'])

PlotMultiple(datasAndFits)
