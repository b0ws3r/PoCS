import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression
import numpy

def GetType(dataset, type):
    dataFilter = dataset['Type'] == type
    filtered_dataset = dataset[dataFilter]
    return filtered_dataset

def GetLogLinearRegression(dataset):
    X = dataset['Weight'].values  # values converts it into a numpy array
    Y = dataset['Record'].values
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

def PlotResults(dataAndFit, gender, type):
    plt.scatter(dataAndFit[0], dataAndFit[1])
    plt.plot(dataAndFit[0], dataAndFit[2], color='red')
    plt.title(gender + '\'s ' + type)
    plt.xlabel("ln(Weight Class)")
    plt.ylabel("ln(Record)")
    plt.savefig(gender+type+'.jpg')
    plt.close()

def GetNormalizedRecords(dataframe, coef, untranformed_intercept):
    intercept = 10 ** (untranformed_intercept)
    arr = numpy.zeros(len(dataframe['Record']))
    for idx in range(0, len(dataframe['Record'] - 1)):
        arr[idx] = 100 * ((dataframe['Record'].values[idx] / (intercept * snatch_df['Weight'].values[idx] ** coef)) - 1)
    return arr

def GetMaxFromNormalized(dataframe):
    dataFilter = dataframe['Normalized'] == numpy.amax(dataframe['Normalized'].values)
    return dataframe[dataFilter]


# Get data from CSV
weightLifting_path = 'WeightLiftingRecords_M.csv'
# weightLifting_path = 'WeightLiftingRecords_W.csv'

weightLifting = pd.read_csv(weightLifting_path)

# Snatch
snatch_df = GetType(weightLifting, 'S')
snatch_lf = GetLogLinearRegression(snatch_df)
PlotResults(snatch_lf, snatch_df['Gender'].iloc[1], 'Snatch')
print('snatch intercept: ' + str(snatch_lf[3]))
print('snatch coef: ' + str(snatch_lf[4]))
snatch_df['Normalized'] = GetNormalizedRecords(snatch_df, snatch_lf[4], snatch_lf[3])

# Clean & Jerk
cleanJerk_df = GetType(weightLifting, 'CJ')
cleanJerk_lf = GetLogLinearRegression(cleanJerk_df)
PlotResults(cleanJerk_lf, cleanJerk_df['Gender'].iloc[1], 'CleanAndJerk')
print('cj intercept: ' + str(cleanJerk_lf[3]) )
print('cj coef: ' + str(cleanJerk_lf[4]) )
cleanJerk_df['Normalized'] = GetNormalizedRecords(cleanJerk_df, cleanJerk_lf[4], cleanJerk_lf[3])

# Total
total_df = GetType(weightLifting, 'T')
total_lf = GetLogLinearRegression(total_df)
PlotResults(total_lf, total_df['Gender'].iloc[1], 'Total')
print('tot intercept: ' + str(total_lf[3]))
print('tot coef: ' + str(total_lf[4]))
total_df['Normalized'] = GetNormalizedRecords(total_df, total_lf[4], total_lf[3])

snatch_max_df = GetMaxFromNormalized(snatch_df)
cleanJerk_max_df = GetMaxFromNormalized(cleanJerk_df)
total_max_df = GetMaxFromNormalized(total_df)

maxFrames = [snatch_max_df, cleanJerk_max_df, total_max_df]
print(maxFrames)