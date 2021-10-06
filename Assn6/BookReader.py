import matplotlib.pyplot as plt
import pandas as pd

from Monktools import statstools, plottools

def clean_and_collect_words(line):
    words = line.split(" ")
    words = list(map(lambda w: w.strip().strip("\"").strip(), words))
    return words


aggwords = []
with open("Data/prideandprejudice.txt") as infile:
    for line in infile:
        aggwords = aggwords + clean_and_collect_words(line)


df = pd.DataFrame(aggwords, columns=["word"])
kNamesAppearingNTimes = df['word'].value_counts(sort=True)
raw_freq = kNamesAppearingNTimes.rename_axis('word').reset_index(name='freq')

kNamesAppearingNTimes = raw_freq['freq'].value_counts(sort=True)
n_k = kNamesAppearingNTimes.rename_axis('freq').reset_index(name='N')

# get zipf and return data
fig, ax = plt.subplots()
x_vals, log_nk = statstools.plot_zipf(ax, list(n_k['N']), 'C0', 'Elephants')

# plot the fit and get the slope back
slope, intercept, r, p, stderr = statstools.plot_fit(ax, x_vals, log_nk, 0.7, 1.4, 'lime')
print(slope)
plt.legend([f"line with alpha = {slope}", "Zipf distribution"], shadow=True)
plt.savefig(f"Plots/prideandprejudics{slope}.jpg")
plt.show()

print("wor")