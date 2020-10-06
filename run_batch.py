"""Handles batch runs.

No need to ever change anything here, just use parameters.py to set up the
experiment, run run_batch.py to execute it, and then run analysis.py to
visualize it.
"""

from model import GTModel
from parameters import params, var_params, iterations, max_steps, run_name

from mesa.batchrunner import BatchRunner
from mesa.datacollection import DataCollector
import pandas as pd


# Don't change this
for key, val in var_params.items():
    params.pop(key)


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


# Save data
data.to_csv(f'data_{run_name}.csv')
step_data.to_csv(f'step_data_{run_name}.csv')
