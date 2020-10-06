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
df = pd.read_csv('step_data_tSNE.csv')
rows = list()
for idx, row in df['strategies'].iteritems():
    rows.append(np.array(json.loads(row)))


# Define plotter
@gif.frame
def plot_transformed(transformed, show=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d(transformed[:, 0], transformed[:, 1], transformed[:, 2],
             np.ones(len(transformed)), np.ones(len(transformed)), np.ones(len(transformed)))
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
for idx, row in enumerate(tqdm(rows)):
    transformed = pca.transform(row)
    frames.append(plot_transformed(transformed))

    if idx > 0 and idx % 100 == 0:
        gif.save(
            frames,
            Path() / f'PCA_{idx}.gif',
            duration=5,
            unit='s',
            between='startend'
        )
        frames = []
        import sys; sys.exit()
