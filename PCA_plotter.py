"""Create a 3D gif of the agent strategies throughout iterations using PCA.

The 4D strategy space is reduced to 3D using PCA for every iteration and
plotted in a 3D scatter plot. The snapshots of each iteration are combined
into a gif. A large number of frames makes the gif creation part crash, so
only every 300 iterations are gif-ed. You can combine them afterwards using
gifsicle:

sudo apt install gifsicle
gifsicle PCA_1.gif, PCA_2.gif, PCA_3.gif > PCA_combined.gif

To use this module, first do a batch run with:
run_name='PCA'
iterations=1

and then run this module.
"""
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa
import pandas as pd
import numpy as np
import json
import gif
from tqdm import tqdm
from pathlib import Path


# Read data
run_name = 'PCA'
df = pd.read_csv(f'step_data_{run_name}.csv')
rows = list()
for idx, row in df['strategies'].iteritems():
    rows.append(np.array(json.loads(row)))


# Define plotter
@gif.frame
def plot_transformed(transformed, show=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(transformed[:, 0], transformed[:, 1], transformed[:, 2])
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)

    if show:
        plt.show()


# Prepare environment
pca = PCA(n_components=3)
gif.options.matplotlib['dpi'] = 300
init_transform = pca.fit_transform(rows[1])

# Create frames
frames = []
gif_num = 1
for idx, row in enumerate(tqdm(rows)):
    transformed = pca.transform(row)
    frames.append(plot_transformed(transformed))

    if idx > 0 and idx % 300 == 0:
        gif.save(
            frames,
            Path() / f'{run_name}_{gif_num}.gif',
            duration=5,
            unit='s',
            between='startend'
        )
        frames = []
        gif_num += 1
        # import sys; sys.exit()
