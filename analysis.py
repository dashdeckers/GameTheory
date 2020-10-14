"""Visualize the data gathered from a batch run.

Must use the same iterations, max_steps and run_name parameter value as the
last batch run used. Could fix this for multiple different datasets by saving
the experiment values as JSON along with the datasets themselves.

Problem for later though.
"""
from parameters import strategy_colors, iterations, max_steps, run_name
import matplotlib.pyplot as plt
import pandas as pd


def plot_strategies(iterations, max_steps, step_data):
    """Plot all strategies over time."""

    # Don't need these columns
    cols = [
        'perc_cooperative_actions', 'n_agents',
        'n_friendlier', 'n_aggressive', 'avg_agent_age',
        'n_neighbors',
    ]

    for i in range(0, iterations):
        row_indices = slice(i * max_steps, (i+1) * max_steps)
        step_data[row_indices].drop(columns=cols).plot(color=strategy_colors)

        # Trick to show an extra string on the legent
        plt.plot([], [], ' ', label='CC|CD|DC|DD')
        plt.legend()

        plt.title('Strategies over time')
        plt.show()


def plot_single_column(iterations, max_steps, step_data, col_name):
    """Plot a single column which can be specified."""
    for i in range(0, iterations):
        row_indices = slice(i * max_steps, (i+1) * max_steps)
        step_data[row_indices][col_name].plot()
        plt.title(f'Showing: {col_name}')
        plt.show()


# Read data
step_data = pd.read_csv(f'step_data_{run_name}.csv', index_col=0)

# Plot data
plot_strategies(iterations, max_steps, step_data)
plot_single_column(
    iterations,
    max_steps,
    step_data,
    'perc_cooperative_actions'
)
