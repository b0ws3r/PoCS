import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression
import numpy

def GetLogLinearRegression(dataset):
    X = dataset['N'].values  # values converts it into a numpy array
    Y = dataset['Speed'].values
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
    plt.title('Men and Women''s 2000 m rowing')
    plt.text(.4,1.24, 'Women''s coef: '+ str(datasAndFits[0][0][4]) + '\nMen''s coef:' + str(datasAndFits[1][0][4]))
    plt.xlabel("log10(Number of oarspeople)")
    plt.ylabel("log10(Speed (km/hr))")
    plt.savefig('Combined.jpg')
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
rowing_womens_record_path = 'Data/Women-Table 1.csv'
rowing_mens_record_path = 'Data/Men-Table 1.csv'
datasAndFits = []

# Women
rowing2000mRecord = pd.read_csv(rowing_womens_record_path)
womens_lf = GetLogLinearRegression(rowing2000mRecord)
datasAndFits.append([womens_lf,'Women'])

# Men
rowing2000mRecord = pd.read_csv(rowing_mens_record_path)

mens_lf = GetLogLinearRegression(rowing2000mRecord)
datasAndFits.append([mens_lf, 'Men'])

PlotMultiple(datasAndFits)
