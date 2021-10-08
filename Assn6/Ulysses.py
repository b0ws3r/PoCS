import pandas as pd
import matplotlib.pyplot as plt
from Monktools import statstools, plottools, ranktools

data = pd.read_csv('Data/ulysses.txt', sep=": ", engine='python')
n_k = ranktools.group_data(data, 'k', 'N')

# calculate rho_est:
# rho_est = (# of unique words)/(# of all words)
rho_est = ranktools.get_simon_rho_estimate(n_k)

# num groups of size 1
print(f"Theoretical Fraction of Groups of size 1: {ranktools.n_1(rho_est)}")
print(f"Empirical Fraction of Groups of size 1: {ranktools.get_fraction_of_groups_of_size_n(n_k, 1)}")
# num groups of size 2
print(f"Theoretical Fraction of Groups of size 2: {ranktools.n_2(rho_est)}")
print(f"Empirical Fraction of Groups of size 2: {ranktools.get_fraction_of_groups_of_size_n(n_k, 2)}")
# num groups of size 3
print(f"Theoretical Fraction of Groups of size 3: {ranktools.n_3(rho_est)}")
print(f"Empirical Fraction of Groups of size 3: {ranktools.get_fraction_of_groups_of_size_n(n_k, 3)}")



