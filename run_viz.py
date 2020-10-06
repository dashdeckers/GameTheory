import math
import random

from model import GTModel

from colour import Color
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule


# In comments: The values from the paper
params = {
    # The map size
    'size': 20,  # 20
    # Initial number of agents to place at the start of a run
    'i_n_agents': 60,  # 60  (supposed to naturally grow to avg 100)
    # Initial amount of energy to give each agent at the start of a run
    'i_energy': 0.5,  # ???
    # Initial strategy for every agent at the start of a run
    'i_strategy': [0.5, 0.5, 0.5, 0.5],  # [0.5] * 4
    # Constant for max population control (cost of surviving)
    'k': -3,  # -3 gives alpha=0 for 100 agents
    # Constant for controlling dying of old age (T+M == Maximum lifespan)
    'T': 100,  # ???
    # Minimum lifespan
    'M': 500,  # ???
    # Minimum energy level to reproduce
    'p': 2,  # ???
    # Mutation 'amplitude'
    'd': 0.05,  # 0.1
    # Whether to spawn children near parents or randomly
    'child_location': 'global',  # 'local'
    # Specify the type of movement allowed for the agents
    'movement': 'global', # 'local-prob', 'local-free', 'global' or 'none'
    # Specify how agents mutate
    'mut_type': 'stochastic', #'numeric' or 'stochastic'
    # Whether to print debug statements
    'debug': False, # 'True' or 'False'

    # Strategies to count
    'strategies_to_count': {
            'ALLC':     [1, 1, 1, 1],
            'ALLD':     [0, 0, 0, 0],
            #'TFT':      [1, 0, 1, 0],
            #'GRIM':     [0.8, 0.2, 0.2, 0.2],
            #'PAVLOV':   [1, 0, 0, 1],
            #'GUILTY':   [0, 0, 1, 0],
            #'BRAT':     [0, 1, 0, 1],
            #'ISSUES':   [0, 1, 1, 1],
            #'DIPLOMAT': [1, 0, 1, 1],
            #'NEGPAV':   [0, 1, 1, 0],
            #'PSYCHO':   [1, 1, 0, 1],
            #'REPEATER': [1, 1, 0, 0],
            #'SWITCHER': [0, 0, 1, 1],
            #'CRYBABY':  [0, 1, 0, 0],
            #'0001':     [0, 0, 0, 1],
            #'1110':     [1, 1, 1, 0],
    },
    # Count tolerance
    'count_tolerance': 0.01,
}

def sigmoid(x):
    return 1 / (1 + math.e ** -x)


def agent_portrayal(agent):
    return {
        'Shape': 'circle',
        'Filled': 'true',
        'Layer': 0,
        'Color': Color(rgb=(0, sigmoid(sum(agent.strategy)), 0)).get_hex(),
        'r': 0.5
    }


grid = CanvasGrid(
    agent_portrayal,
    params['size'],
    params['size'],
    500,
    500,
)
total_chart = ChartModule([
    {'Label': 'n_agents',
     'Color': 'Black'},
])
# strategy_sum_chart = ChartModule([
#     {'Label': 'n_friendlier',
#      'Color': 'Green'},
#     {'Label': 'n_aggressive',
#      'Color': 'Red'},
# ])
perc_chart = ChartModule([
    {'Label': 'perc_cooperative_actions',
     'Color': 'Green'},
])

strategy_colors = [
    'Green', 'Red', 'Yellow', 'Orange', 'Blue',
    'Aqua', 'Black', 'Fuchsia', 'Gray', 'Lime',
    'Maroon', 'Navy', 'Olive', 'Purple', 'Silver', 'Teal'
]
strategy_chart = ChartModule([
    {'Label': label, 'Color': color}
    for label, color in
    zip(params['strategies_to_count'].keys(), strategy_colors)
])


server = ModularServer(
    GTModel,
    [grid, total_chart, perc_chart, strategy_chart],
    'Prisoners Dilemma Model',
    params,
)
server.port = 8522
server.launch()
