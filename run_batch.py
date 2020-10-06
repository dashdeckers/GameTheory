from model import GTModel
from parameters import params

import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner
from mesa.datacollection import DataCollector
import pandas as pd

# Define parameters
var_params = {
    'i_n_agents': [60],
    'd': [0.5],
    # 'k': range(-2, 1),
    # 'p': [i/10 for i in range(1, 11)],
}
for key, val in var_params.items():
    params.pop(key)

run_name = 'tSNE'
iterations = 1
max_steps = 1000

# Run experiments
batch_runner = BatchRunner(
    GTModel,
    var_params,
    params,
    # iterations per setting
    iterations=iterations,
    # steps per iteration
    max_steps=max_steps,
    # collect step data
    model_reporters={'DC': lambda m: m.datacollector},
)

batch_runner.run_all()

# Collect data
data = batch_runner.get_model_vars_dataframe()
step_data = pd.DataFrame()

for i in range(len(data['DC'])):

    # Unpack the datacollectors in the data df into a step_data df
    if isinstance(data['DC'][i], DataCollector):
        run_data = data['DC'][i].get_model_vars_dataframe()
        step_data = step_data.append(run_data, ignore_index=True)

data.to_csv(f'data_{run_name}.csv')
step_data.to_csv(f'step_data_{run_name}.csv')


# Plot data
def n_plots(start, n_plots, iterations, max_steps, step_data):
    for i in range(start, n_plots * iterations, iterations):
        step_data[i * max_steps: (i+1) * max_steps].drop(
            # Don't need these columns
            columns=['perc_cooperative_actions', 'n_agents',
                     'n_friendlier', 'n_aggressive']
        ).plot()

        plt.show()


# n_plots(0, 3, iterations, max_steps, step_data)
