import matplotlib
import pandas as pd
from Monktools import plottools, ranktools

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

# Get data from CSV
path = 'Data/vocab_cs_mod.csv'
all_data = pd.read_csv(path)

fig2, ax = plt.subplots()
ax.scatter(np.log10(list(all_data['k'])), np.log10(list(all_data['N'])))
plottools.plot_fit(ax, np.log10(list(all_data['k'])), np.log10(list(all_data['N'])), 0.5, color='red')

figz, axz = plt.subplots()
x_vals, log_nk = ranktools.plot_zipf(axz, list(all_data['N']))
slope_new, intercept_new, r_new, p_new, stderr_new = plottools.plot_fit(axz, x_vals, log_nk, low_fit=2, high_fit=4.5, color='red')
print(f'slope: {slope_new}')
print(f'variance: {stderr_new ** 2}')
axz.legend()
figz.savefig(f"Plots/zipfy_og.png")


def n_greaterthan_k(k):
    n_gk = 3.46 * (10 ** 8) * k ** (-0.661)
    return n_gk


# number of words that appear more than once given by:
n_twice = n_greaterthan_k(1)
# this means that that for part c, we have at least
known_num_words_to_200 = sum(list(all_data['N']))
print(f'known words count {str(known_num_words_to_200)}')

calc = 0
artificial_data = pd.DataFrame(columns=['n', 'k'])
for i in range(3, 202):
    # number of words occurring more than k times
    k = 203 - i
    if k == 200: continue
    # n_k = n_greaterthan_k(i) - n_greaterthan_k(i-2)
    # n_k = n_greaterthan_k(k - 1) - calc
    n_k = n_greaterthan_k(k - 1) - n_greaterthan_k(k + 1)
    calc = calc + n_k
    # print(k)
    # print(n_k)
    artificial_data = artificial_data.append({'n': n_k, 'k': k}, ignore_index=True)
    all_data = all_data.append({'N': n_k, 'k': k}, ignore_index=True)

# ranktools.plot_zipf(ax, list(artificial_data['n']), color='red')

ax.scatter(np.log10(list(artificial_data['k'])), np.log10(list(artificial_data['n'])))
slope, intercept, r, p, stderr = plottools.plot_fit(ax, np.log10(list(artificial_data['k'])),
                                                    np.log10(list(artificial_data['n'])), 0, 2, color='purple')
ax.set_title("Artificial fit for google words data for N<200")
# ax.legend()
print(f'slope: {slope}')
print(f'variance: {stderr ** 2}')
fig2.savefig(f"Plots/google_word_hypothetical_fit.png")
# fit for zipf alpha = 1/(gamma-1)
# the problem gives us gamma = −0.661


# the wholeee fit
fig3, ax3 = plt.subplots()
slope_new, intercept_new, r_new, p_new, stderr_new = plottools.plot_fit(ax, np.log10(list(artificial_data['n'])),
                                                                        np.log10(list(artificial_data['k'])), 0.5, 6.8,
                                                                        color='blue')
print(f'slope: {slope_new}')
print(f'variance: {stderr_new ** 2}')
# ax3.legend()
fig3.savefig(f"Plots/google_word_hypothetical_combined_fit.png")

# for now, estimate words that appear once as .001
funny_guys = n_greaterthan_k(.000001) - (calc + known_num_words_to_200)
total_words = (sum(list(all_data['N'] * all_data['k'])) + funny_guys)


# (i)The hypothetical fraction of words that appear once out of all words
# (think of words as organisms or tokens here),
fraction_appearing_once = funny_guys / total_words
print(f"total unique words in dataset: {total_words}")
print(f"fraction appearing once: {fraction_appearing_once}")

# (ii) fraction_appearing_once = funny_guys/ (sum(list(dataframe['N'])) + funny_guys)
# species/type level
total_word_groups = (funny_guys + calc) + known_num_words_to_200
fraction_appearing_once_in_google_ds = funny_guys / total_word_groups
print(f"fraction appearing once in google's dataset: {fraction_appearing_once_in_google_ds}")

# (iii) fraction missing
num_199_to_1 = (sum(list(artificial_data['n'] * artificial_data['k'])) + funny_guys)
print(f'num from 199 to 1: {num_199_to_1}')
fraction_missing = num_199_to_1 / total_words
print(f"fraction missing: {fraction_missing}")



figz2, axz2 = plt.subplots()
x_vals, log_nk = ranktools.plot_zipf(axz2, list(all_data['N']))
slope_new, intercept_new, r_new, p_new, stderr_new = plottools.plot_fit(axz2, x_vals, log_nk, low_fit=0, high_fit=2, color='red')
print(f'slope: {slope_new}')
print(f'variance: {stderr_new ** 2}')
axz.legend()
figz.savefig(f"Plots/zipfy_new.png")
