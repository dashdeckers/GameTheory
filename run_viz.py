import math

from model import GTModel

from colour import Color
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, PieChartModule


# In comments: The values from the paper
params = {
    # The map size
    'size': 20,  # 20
    # Initial number of agents to place at the start of a run
    'i_n_agents': 60,  # 60  (supposed to naturally grow to avg 100)
    # Initial strategy for every agent at the start of a run
    'i_strategy': [0.5, 0.5, 0.5, 0.5],  # [0.5] * 4
    # Initial amount of energy to give each agent at the start of a run
    'i_energy': 0.5,  # ???
    # Constant for max population control (cost of surviving)
    'k': -4,  # ???
    # Constant for controlling dying of old age (T+M == Maximum lifespan)
    'T': 10,  # ???
    # Minimum lifespan
    'M': 5,  # ???
    # Minimum energy level to reproduce
    'p': 0.5,  # ???
    # Mutation 'amplitude'
    'd': 0.3,  # 0.1
    # Whether to spawn children near parents or randomly
    'child_location': 'local',  # 'global'
    # Specify the type of movement allowed for the agents
    'movement': 'local-prob',  # 'local-prob'
    # Whether to print debug statements
    'debug': True,

    # Strategies to count
    'strategies_to_count': {
            'ALLC':     [1, 1, 1, 1],
            'ALLD':     [0, 0, 0, 0],
            'TFT':      [1, 0, 1, 0],
            'GRIM':     [1, 0, 0, 0],
            'PAVLOV':   [1, 0, 0, 1],
            'GUILTY':   [0, 0, 1, 0],
            'BRAT':     [0, 1, 0, 1],
            'ISSUES':   [0, 1, 1, 1],
            'DIPLOMAT': [1, 0, 1, 1],
            'NEGPAV':   [0, 1, 1, 0],
            'PSYCHO':   [1, 1, 0, 1],
            'REPEATER': [1, 1, 0, 0],
            'SWITCHER': [0, 0, 1, 1],
            'CRYBABY':  [0, 1, 0, 0],
            '0001':     [0, 0, 0, 1],
            '1110':     [1, 1, 1, 0],
    },
    # Count tolerance
    'count_tolerance': 0.3,
}


def agent_portrayal(agent):
    def sigmoid(x):
        return 1 / (1 + math.e ** -x)

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
    'Maroon', 'Green', 'Red', 'Yellow', 'Orange', 'Blue',
    'Aqua', 'Black', 'Fuchsia', 'Gray', 'Lime',
    'Maroon', 'Navy', 'Olive', 'Purple', 'Silver',
    'Teal',
]
strategy_chart = PieChartModule([
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
