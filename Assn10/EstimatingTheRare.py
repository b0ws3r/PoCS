import matplotlib
from typing import List
import pickle
import numpy
import pandas as pd
from Monktools import plottools, ranktools

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np


# Get data from CSV
path = 'Data/vocab_cs_mod.csv'
dataframe = pd.read_csv(path)

fig2, ax = plt.subplots()
# x_vals, log_nk = ranktools.plot_zipf(ax, list(dataframe['N']))
ax.scatter(np.log10(list(dataframe['N'])), np.log10(list(dataframe['k'])))
plottools.plot_fit(ax, np.log10(list(dataframe['N'])), np.log10(list(dataframe['k'])), 0.5, color='red')

def n_greaterthan_k(k):
    n_gk = 3.46* (10**8) * k ** (-0.661)
    return n_gk


#number of words that appear more than once given by:
n_twice = n_greaterthan_k(1)
# this means that that for part c, we have at least
known_num_words_to_200 = sum(list(dataframe['N']))
num_199_to_2 = n_twice - known_num_words_to_200

print(f'known words count {str(known_num_words_to_200)}')
calc=0
df = pd.DataFrame(columns=['n','k'])
for i in range(3, 200):
    # number of words occurring more than k times
    k=203-i
    #n_k = n_greaterthan_k(i) - n_greaterthan_k(i-2)
    # n_k = n_greaterthan_k(k-1) - (known_num_words_to_200 + calc)
    n_k = n_greaterthan_k(k - 1) - n_greaterthan_k(k + 1)
    calc= calc+n_k
    print(k)
    print(n_k)
    df = df.append({'n': n_k, 'k':k}, ignore_index=True)

# ranktools.plot_zipf(ax, list(df['n']), color='red')
ax.scatter(np.log10(list(df['n'])), np.log10(list(df['k'])))
slope, intercept, r, p, stderr = plottools.plot_fit(ax, np.log10(list(df['n'])), np.log10(list(df['k'])), 5, 6.8, color='purple')
ax.set_title("fit with")
ax.legend()
fig2.savefig(f"Plots/google_zipf.png")
# fit for zipf alpha = 1/(gamma-1)
# the problem gives us gamma = −0.661

