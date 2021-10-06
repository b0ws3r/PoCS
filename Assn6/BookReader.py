import pandas as pd


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
k_vs_n = kNamesAppearingNTimes.rename_axis('word').reset_index(name='k')

print("wor")