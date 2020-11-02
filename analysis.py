"""Visualize the data gathered from a batch run.

Uses the same run_name as defined in parameters.py but you can also just
redefine the variable to plot a different dataset.
"""
from parameters import strategy_colors, run_name
import matplotlib.pyplot as plt
import pandas as pd
import json
import math
from pathlib import Path
import gc


def get_params(run_name):
    # Load the config file
    with open(Path() / run_name / 'config.json', 'r') as file:
        params = json.load(file)

    # How many different settings? Every possible combination of settings
    # as defined in the var_params dict: Take the product.
    params['n_settings'] = math.prod(
        [len(list(setting)) for _, setting in params['var_params'].items()]
    )
    return params


def get_data(params, column_filter=None):
    # Read the data in chunks (one chunk is all iterations of a setting)
    run_name = params['run_name']
    chunksize = params['max_steps'] * params['iterations']

    data = pd.read_csv(Path() / run_name / 'data.csv')
    for step_data_chunk in pd.read_csv(
                Path() / run_name / 'step_data.csv',
                usecols=column_filter,
                chunksize=chunksize,
            ):

        gc.collect()

        # Fix first column bug in case it is a problem
        first_column = step_data_chunk.columns.values[0]
        if first_column == 'Unnamed: 0':
            step_data_chunk.set_index([first_column], inplace=True)
            step_data_chunk.index.names = [None]

        yield (data, step_data_chunk)


def plot(params, plot_list='strategies', average=True):
    """Plots the data.

    Just pass the relevant data and step_data and specify what to plot.
    The 'plot' parameter can be either 'strategies', or a list of column names
    to plot. Toggle average to plot either the averages across iterations/runs
    or each single iteration/run.
    """
    def column_filter(column):
        if plot_list == 'strategies':
            return column not in [
                'perc_cooperative_actions', 'n_agents',
                'n_friendlier', 'n_aggressive', 'avg_agent_age',
                'n_neighbors', 'avg_delta_energy',
            ]
        else:
            return column in plot_list

    plot_folder = Path() / params['run_name'] / 'plots'
    try:
        plot_folder.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        pass

    data_iter = get_data(params, column_filter=column_filter)
    for idx, (data, step_data) in enumerate(data_iter):

        if average:
            # get the parameter values we are plotting for
            data_idx = idx * params['iterations']
            setting_values = list(
                data.loc[data_idx][params['var_params'].keys()].items()
            )
            # plot the mean across iterations
            step_data.groupby(
                step_data.index % params['max_steps']
            ).mean().plot(color=strategy_colors)
            plt.title(f'Showing average {plot_list} for:\n{setting_values}')
            plt.legend(ncol=2)
            if 'perc_cooperative_actions' in plot_list:
                plt.ylim(0, 1)
            if plot_list == 'strategies':
                plt.ylim(0, 50)
            filename = str(plot_list) + str(setting_values).replace('.', '_')
            plt.savefig(plot_folder / filename)
            plt.show()

        else:
            for i in range(0, params['iterations']):
                # get the parameter values we are plotting for
                setting_values = list(
                    data.loc[i][params['var_params'].keys()].items()
                )
                # plot the values
                rows = slice(
                    i * params['max_steps'],
                    (i+1) * params['max_steps']
                )
                step_data[rows].plot(color=strategy_colors)
                plt.title(f'Showing {plot_list} for:\n{setting_values}')
                plt.legend(ncol=2)
                plt.show()


if __name__ == '__main__':
    # run_name = 'BIG_RUN_P'  # noqa
    columns = ['perc_cooperative_actions']
    params = get_params(run_name)

    plot(params, plot_list=columns)
    plot(params, plot_list='strategies')
