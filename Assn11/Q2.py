import networkx as nx
import matplotlib
import pandas as pd
import matplotlib.ticker as ticker
from Monktools import plottools, ranktools
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np


df = pd.DataFrame(columns=['p', 'c_p','l_p'])
probabilities = np.geomspace(0.0001, 1, 14)
for p in probabilities:
    g = nx.generators.random_graphs.watts_strogatz_graph(1000, 10, p)
    c_p = nx.algorithms.cluster.average_clustering(g)  #
    c_0 = nx.algorithms.cluster.square_clustering(g)
    l_p = nx.average_shortest_path_length(g)  #
    df = df.append({'p': p, 'c_p': c_p, 'l_p': l_p}, ignore_index=True)

df = df.sort_values(by=['p'])
c_0 = df['c_p'][0]
l_0 = df['l_p'][0]
df['c_p_norm'] = df['c_p']/c_0
df['l_p_norm'] = df['l_p']/l_0
df['p_log'] = np.log10(df['p'])
fig, ax = plt.subplots()
ax.scatter(df['p_log'], df['c_p_norm'], marker='s', label='C_p/C_0')
ax.scatter(df['p_log'], df['l_p_norm'], marker='.', label='L_p/L_0')
ax.set_xlabel('log10(p)')
# x = [10**(-4), 10**(-3),10**(-2),10**(-1),1]
# ax.set_xticks(np.log10(x))
ax.legend()

# ax.xaxis.set_major_locator(ticker.FixedLocator(x))

fig.savefig('Plots/WattsStrogatz.png')

