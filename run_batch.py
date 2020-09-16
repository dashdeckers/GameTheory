from model import GTModel
from reporter_funcs import hawk_count, dove_count

from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt


# Define parameters
fix_params = {
    'n_agents': 12,
    'strategies': ['Hawk', 'Dove'],
    'init_pop': 'Hawk invader',
}

var_params = {
    'n_food': range(10, 20),
}


# Run experiments
batch_runner = BatchRunner(
    GTModel,
    var_params,
    fix_params,
    iterations=300,
    max_steps=50,
    model_reporters={
        "Hawks": hawk_count,
        "Doves": dove_count,
    },
)

batch_runner.run_all()
data = batch_runner.get_model_vars_dataframe()


# Plot results
plt.hist(
    [data['Hawks'], data['Doves']],
    color=['r', 'g'],
    label=['Hawks', 'Doves'],
)
init_pop = fix_params['init_pop']
plt.title(f'Population sizes after 50 steps ({init_pop})')
plt.xlabel('Population size')
plt.ylabel('Counts')
plt.legend()
plt.show()
