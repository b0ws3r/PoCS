import pandas
import pandas as pd  # To read data
from Monktools import statstools, plottools
import numpy

# Get data from CSV
path = 'Data/vocab_cs_mod.csv'

dataframe = pd.read_csv(path)

# raw unfiltered
# linear_fit = statstools.get_linear_regression(dataframe, 'k', 'N', False)
# plottools.plot_results(linear_fit, 'k', 'N_k', 'Plot of count of words (N_k) appearing k times', False)

arr = numpy.zeros(len(dataframe['k']))
for idx in range(0, len(dataframe['k'] - 1)):
    # since gamma is 10, x^(-10+1) = x^-9
    arr[idx] = dataframe['N'].values[idx]**(1/9)
dataframe['ccdf'] = arr

# plot word frequency as a function of zipf rank - group data so that we don't have to plot 14mil points
raw_dataframe = statstools.get_dataframe('Data/rawwwordfreqs.csv')

# df = raw_dataframe.groupby(['k']).sum().reset_index()
# plot = df['k'].plot(kind='hist')

grouped_df = pd.cut(raw_dataframe['k'], bins=numpy.linspace(0, 10**6, 10**4)).value_counts()
idx = pandas.IntervalIndex(grouped_df.index)

df1 = pd.DataFrame(data=grouped_df.index, columns=['group'])
df2 = pd.DataFrame({'intervals': idx, 'left': idx.left, 'right': idx.right})
df3 = pd.DataFrame(data=grouped_df.values, columns=['numberofwordsingroup'])
df = pd.merge(df1, df2, left_index=True, right_index=True)
df = pd.merge(df, df3, left_index=True, right_index=True)

plottools.plot_results(df, 'numberofwordsingroup', 'right', 'Zipf plot', False)

print('wow')
#
# print('avg: ' + str(avg))
# print('sigma: ' + str(numpy.sqrt(variance)))
