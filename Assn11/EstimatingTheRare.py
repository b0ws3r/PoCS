import matplotlib
import pandas as pd
from Monktools import plottools, ranktools

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

# Get data from CSV
path = 'Data/vocab_cs_mod.csv'
all_data = pd.read_csv(path)

avg = np.sum(all_data['N'] * all_data['k']) / np.sum(all_data['N'])
variance = np.sum((all_data['N'] * (all_data['k'] - avg) ** 2)) / np.sum(all_data['N'])

fig2, ax = plt.subplots()
ax.scatter(np.log10(list(all_data['k'])), np.log10(list(all_data['N'])))
plottools.plot_fit(ax, np.log10(list(all_data['k'])), np.log10(list(all_data['N'])), 2, 4.5, color='red')

# Plot the original data
figz, axz = plt.subplots()
x_vals, log_nk = ranktools.plot_zipf(axz, list(all_data['N']))
slope_new, intercept_new, r_new, p_new, stderr_new = plottools.plot_fit(axz, x_vals, log_nk, low_fit=2, high_fit=4.5, color='red')

axz.legend()
figz.savefig(f"Plots/zipfy_og.png")


def n_greaterthan_k(k):
    n_gk = 3.46 * (10 ** 8) * k ** (-0.661)
    return n_gk


artificial_data = pd.DataFrame(columns=['n', 'k'])
for i in range(3, 202):
    # number of words occurring more than k times
    k = 203 - i
    if k == 200: continue
    n_k = n_greaterthan_k(k - 1) - n_greaterthan_k(k + 1)
    artificial_data = artificial_data.append({'n': n_k, 'k': k}, ignore_index=True)
    all_data = all_data.append({'N': n_k, 'k': k}, ignore_index=True)

ax.scatter(np.log10(list(artificial_data['k'])), np.log10(list(artificial_data['n'])))
slope, intercept, r, p, stderr = plottools.plot_fit(ax, np.log10(list(artificial_data['k'])),
                                                    np.log10(list(artificial_data['n'])), 0, 2, color='purple')

ax.set_title("Artificial fit for google words data for N<200")
ax.set_xlabel('log10(k)')
ax.set_ylabel('log10(N)')
ax.legend()
fig2.savefig(f"Plots/google_word_hypothetical_fit.png")


funny_guys = 10**intercept
all_data = all_data.append({'N': funny_guys, 'k': 1}, ignore_index=True)

total_words = (sum(list(all_data['N'] * all_data['k'])))

# (i)The hypothetical fraction of words that appear once out of all words
# (think of words as organisms or tokens here),
fraction_appearing_once = funny_guys / total_words
print(f"total unique words in dataset: {funny_guys}")
print(f"fraction appearing once: {fraction_appearing_once}")

avg = np.sum(all_data['N'] * all_data['k']) / np.sum(all_data['N'])
variance = np.sum((all_data['N'] * (all_data['k'] - avg) ** 2)) / np.sum(all_data['N'])
print('avg: ' + str(avg))
print('sigma: ' + str(np.sqrt(variance)))


# the wholeee fit
fig3, ax3 = plt.subplots()
ax3.scatter(np.log10(list(all_data['k'])), np.log10(list(all_data['N'])))
slope_new, intercept_new, r_new, p_new, stderr_new = plottools.plot_fit(ax3, np.log10(list(all_data['k'])),
                                                                        np.log10(list(all_data['N'])), 0.0, 4.5,
                                                                        color='yellow')

ax3.set_xlabel('log10(k)')
ax3.set_ylabel('log10(N)')
ax3.legend()
fig3.savefig(f"Plots/google_word_hypothetical_combined_fit.png")

# (ii) fraction_appearing_once = funny_guys/ (sum(list(dataframe['N'])) + funny_guys)
# species/type level
total_word_groups = np.sum(all_data['N'])
fraction_appearing_once_in_google_ds = funny_guys / total_word_groups
print(f"fraction appearing once in google's dataset: {fraction_appearing_once_in_google_ds}")

# (iii) fraction missing
num_199_to_1 = (sum(list(artificial_data['n'] * artificial_data['k']))) + funny_guys
print(f'num from 199 to 1: {num_199_to_1}')
fraction_missing = num_199_to_1 / total_words
print(f"fraction missing: {fraction_missing}")

