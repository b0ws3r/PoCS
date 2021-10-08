import matplotlib.pyplot as plt
import pandas as pd

from Monktools import statstools, plottools, ranktools


def clean_and_collect_words(line_of_text):
    words = line_of_text.split(" ")
    words = list(map(lambda w: w.strip().strip("\"").strip(), words))
    return words


def read_book(path):
    words_in_book = []
    with open(path) as infile:
        for line in infile:
            words_in_book = words_in_book + clean_and_collect_words(line)
    return words_in_book


def Q_6(words_in_book):
    df = pd.DataFrame(words_in_book, columns=["word"])
    words_with_freqs = ranktools.group_data(df, 'word', 'k')
    n_k = ranktools.group_data(words_with_freqs, 'k', 'N')

    rho_est = ranktools.get_simon_rho_estimate(n_k)

    # num groups of size 1
    k1 = [1, ranktools.n_1(rho_est), ranktools.get_fraction_of_groups_of_size_n(n_k, 1)]
    k2 = [2, ranktools.n_2(rho_est), ranktools.get_fraction_of_groups_of_size_n(n_k, 2)]
    k3 = [3, ranktools.n_3(rho_est), ranktools.get_fraction_of_groups_of_size_n(n_k, 3)]
    table = [k1, k2, k3]
    df = pd.DataFrame(table, columns=['k', 'theory', 'empirical'])
    latex = df.to_latex()
    print(latex)

# get the words out of pride and prejudice
words_in_book = read_book("Data/prideandprejudice.txt")
Q_6(words_in_book)

# get the words out of pride and prejudice
words_in_book = read_book("Data/comtedemontecristo.txt")
Q_6(words_in_book)


