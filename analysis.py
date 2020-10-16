"""Visualize the data gathered from a batch run.

Must use the same iterations, max_steps and run_name parameter value as the
last batch run used. Could fix this for multiple different datasets by saving
the experiment values as JSON along with the datasets themselves.

Problem for later though.
"""
from parameters import strategy_colors, run_name
import matplotlib.pyplot as plt
import pandas as pd
import json
import math


def get_params(run_name):
    # Load the config file
    with open(f'{run_name}_config.json', 'r') as file:
        params = json.load(file)

    # How many different settings? Every possible combination of settings
    # as defined in the var_params dict: Take the product.
    params['n_settings'] = math.prod(
        [len(list(setting)) for _, setting in params['var_params'].items()]
    )
    return params


def get_data(run_name):
    data = pd.read_csv(f'{run_name}_data.csv')
    step_data = pd.read_csv(f'{run_name}_step_data.csv')

    # Fix for the FutureWarning about pairwise comparisons from numpy
    data.set_index([data.columns.values[0]], inplace=True)
    data.index.names = [None]

    step_data.set_index([step_data.columns.values[0]], inplace=True)
    step_data.index.names = [None]
    return data, step_data


def plot(params, data, step_data, plot='strategies', average=True):
    """Plots the data.

    Just pass the relevant data and step_data and specify what to plot.
    The 'plot' parameter can be either 'strategies', 'cooperation' or the name
    of a specific column to plot. Toggle average to plot either the averages
    across iterations/runs or each single iteration/run.
    """
    if plot == 'cooperation':
        columns = ['perc_cooperative_actions']
    elif plot == 'strategies':
        columns = [
            c for c in step_data.columns.to_list() if c not in [
                'perc_cooperative_actions', 'n_agents',
                'n_friendlier', 'n_aggressive', 'avg_agent_age',
                'n_neighbors', 'avg_delta_energy',
            ]
        ]
    else:
        columns = plot

    if average:
        # split into one dataframes per setting (parameter configuration)
        split_size = params['max_steps'] * params['iterations']
        setting_splits = [
            step_data.loc[i:i+split_size-1, :]
            for i in range(0, len(step_data), split_size)
        ]
        # assert all(len(s) == split_size for s in setting_splits)
        # assert len(setting_splits) == params['n_settings']

        for idx, setting in enumerate(setting_splits):
            # get the parameter values we are plotting for
            data_idx = idx * params['iterations']
            setting_values = list(
                data.loc[data_idx][params['var_params'].keys()].items()
            )
            # plot the mean across iterations
            setting[columns].groupby(
                setting.index % params['max_steps']
            ).mean().plot(color=strategy_colors)
            plt.title(f'Showing average {plot} for:\n{setting_values}')
            plt.legend(ncol=2)
            plt.show()

    else:
        for i in range(0, params['iterations'] * params['n_settings']):
            # get the parameter values we are plotting for
            setting_values = list(
                data.loc[i][params['var_params'].keys()].items()
            )
            # plot the values
            rows = slice(i * params['max_steps'], (i+1) * params['max_steps'])
            step_data[rows][columns].plot(color=strategy_colors)
            plt.title(f'Showing {plot} for:\n{setting_values}')
            plt.legend(ncol=2)
            plt.show()


if __name__ == '__main__':
    # Read data
    # run_name = 'density'  # noqa
    data, step_data = get_data(run_name)
    params = get_params(run_name)

    # Plot data
    print(data.head())
    plot(params, data, step_data, 'strategies')
    # plot(params, data, step_data, 'strategies', average=False)
    plot(params, data, step_data, 'perc_cooperative_actions')
