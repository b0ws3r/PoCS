import pandas as pd
import matplotlib.pyplot as plt
from Monktools import statstools, plottools


def group_data(dataframe, column):
    k_n = dataframe[column].value_counts(sort=True)
    k_n = k_n.rename_axis('k').reset_index(name='N')
    return k_n
# We will see how many different types of elephants reproduce w/ diff colors


data = pd.read_csv('Data/ulysses.txt', sep=": ", engine='python')
n_k = group_data(data, 'k')

# get zipf and return data
fig, ax = plt.subplots()
x_vals, log_nk = statstools.plot_zipf(ax, list(n_k['N']), 'C0', 'Elephants')

# plot the fit and get the slope back
slope, intercept, r, p, stderr = statstools.plot_fit(ax, x_vals, log_nk, 1.498,1.647, 'lime')
print(slope)
plt.title("Ulysses Zipf distribution")
plt.legend([f"line with alpha = {slope}", "Zipf distribution"], shadow=True)
plt.show()
plt.savefig(f"Plots/ulysses{slope}.jpg")



