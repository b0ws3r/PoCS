import scipy as sp
from scipy import special
import numpy as np

# part a
# For n → ∞,
# use some computation tool to determine that
# α ≈ 1.73 for a= 1. (Recall: we expect α<1 for γ >2)

x = np.linspace(1, 2, 100000)
result = sp.special.zetac(x)

filter_arr = []
for idx, val in enumerate(x):
    if result[idx] - .0001 < 1 < result[idx] + .0001:
        filter_arr.append(True)
        print(val)
    else:
        filter_arr.append(False)
filtered_results = result[filter_arr]

print(len(filtered_results))

