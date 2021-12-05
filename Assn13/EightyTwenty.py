import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
from scipy import ndimage
from Monktools import plottools, ranktools


gamma = 2.1278
e = (gamma-2)/(gamma-1)


def f(x):
    return 1-(1-x)**e


THETA_POP = "\u03F4 Population"
THETA_WEALTH = "\u03F4 Wealth"
x = np.arange(0.0, 1.0, 0.001)
plt.plot(x, f(x))
plt.plot(x,x, 'r--')
plt.xlabel(THETA_POP)
plt.ylabel(THETA_WEALTH)


# plt.show()
plt.savefig('Data/pop_v_wealth')

x_t = np.arange(0.0, 1.0, 0.1)
x_t = np.append(x_t, [0.99] )
ser = [(x, f(x)) for x in x_t]
df = pd.DataFrame.from_records(ser, index=None, columns=[THETA_POP, THETA_WEALTH])
latex = df[[THETA_POP,THETA_WEALTH]].to_latex(index=None)
print(latex)