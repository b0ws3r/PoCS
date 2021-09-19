import pandas
import pandas as pd  # To read data
from Monktools import statstools, plottools
import numpy

# Get data from CSV
dataframe = statstools.get_dataframe('Data/names-boys1952.csv')

# raw unfiltered
linear_fit = statstools.get_linear_regression(dataframe, 'Name', 'Frequency', True)
gamma = -1 * linear_fit[4]
# gamma = 10**(-1 * coef)

arr = numpy.zeros(len(dataframe['Name']))
for idx in range(0, len(dataframe['Name'])- 1):
    arr[idx] = dataframe['Frequency'].values[idx]**(1/gamma + 1)
dataframe['ccdf'] = arr


# plot word frequency as a function of zipf rank - group data so that we don't have to plot 14mil points

# grouped_df = pd.cut(dataframe['k'], bins=numpy.linspace(0, 10**6, 10**4)).value_counts()
# idx = pandas.IntervalIndex(grouped_df.index)
#
# df1 = pd.DataFrame(data=grouped_df.index, columns=['group'])
# df2 = pd.DataFrame({'intervals': idx, 'left': idx.left, 'right': idx.right})
# df3 = pd.DataFrame(data=grouped_df.values, columns=['numberofwordsingroup'])
# df = pd.merge(df1, df2, left_index=True, right_index=True)
# df = pd.merge(df, df3, left_index=True, right_index=True)
#
# plottools.plot_results(df, 'numberofwordsingroup', 'right', 'Zipf plot', False)

print('wow')
#
# print('avg: ' + str(avg))
# print('sigma: ' + str(numpy.sqrt(variance)))
