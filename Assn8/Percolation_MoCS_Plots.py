import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import cm
from IPython import display
from time import sleep

# Random walker
from scipy import ndimage


def run_random_walker(world, position, history, steps):
    N1 = world.shape[0]
    N2 = world.shape[1]
    (i, j) = position
    for k in range(steps):  # for every step
        world[position] = 0.67
        (i, j) = position
        die = random.uniform(0, 1)
        if die < 0.25:  # right step
            position = (i, (j + 1) % N2)
        elif die < 0.5:  # bottom step
            position = ((i - 1) % N1, j)
        elif die < 0.75:  # left step
            position = (i, (j - 1) % N2)
        else:  # top step
            position = ((i + 1) % N1, j)
        world[position] = 1
        history.append(position)

    return world, position, history


# Site percolation
def run_percolation(world, probability):
    N1 = world.shape[0]
    N2 = world.shape[1]
    for i in range(N1):  # for cell in every row
        for j in range(N2):  # and every column
            die = random.uniform(0, 1)
            if die < probability:
                world[(i, j)] = 1
            else:
                world[(i, j)] = 0

    return (world)


# Parameters
N1, N2 = 512, 512  # height, width
# occupation probability
probability = 0.52  # @param {type:"slider", min:0, max:1, step:0.01}
# initial conditions of zero
world = np.zeros((N1, N2))

world = run_percolation(world, probability)  # run model

# Set up the figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
ax1.set_ylim(0, N1)
ax1.set_xlim(0, N2)
ax2.set_ylim(0, N1)
ax2.set_xlim(0, N2)
ax1.set_aspect('equal')
ax2.set_aspect('equal')

# filter largest cluster
structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]  # define connection
label_world, nb_labels = ndimage.label(world, structure)  # label clusters
sizes = ndimage.sum(world, label_world, range(nb_labels + 1))
mask = sizes >= sizes.max()
binary_img = mask[label_world]

# Plot the world
ax1.imshow(world, cmap=plt.get_cmap(cm.bone), origin='lower')
ax2.imshow(binary_img, cmap=plt.get_cmap(cm.bone), origin='lower')

# Add label
ax1.text(2, N1 + 5, f'Site percolation with probability {probability}', color='Orange', fontsize=18)
ax2.text(2, N1 + 5, f'Largest cluster found of size {sizes.max()}', color='Orange', fontsize=18)
plt.show()
