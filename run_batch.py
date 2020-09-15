from model import GTModel
from reporter_funcs import all_c_score, all_d_score, tft_score

from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt


# Define parameters
fix_params = {
    'size': 10,
    'strategies': ['ALLC', 'ALLD', 'TFT'],
}

var_params = {
    'n_agents': range(5, 11),
}


# Run experiments
batch_runner = BatchRunner(
    GTModel,
    var_params,
    fix_params,
    # iterations per setting
    iterations=300,
    # steps per iteration
    max_steps=50,
    model_reporters={
        "ALLC": all_c_score,
        "ALLD": all_d_score,
        "TFT": tft_score,
    },
)

batch_runner.run_all()
data = batch_runner.get_model_vars_dataframe()


# Plot results
plt.hist(
    [data[strategy] for strategy in fix_params['strategies']],
    color=['g', 'r', 'y'],
    label=fix_params['strategies']
)
plt.title('Total scores of strategies after 50 steps (random proportions)')
plt.xlabel('Total score')
plt.ylabel('Counts')
plt.legend()
plt.show()
