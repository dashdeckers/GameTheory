import math

from model import GTModel

from colour import Color
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule


params = {
    # The map size
    'size': 20,
    # Initial number of agents to place at the start of a run
    'i_n_agents': 100,
    # Initial strategy for every agent at the start of a run
    'i_strategy': [0.5, 0.5, 0.5, 0.5],
    # Initial amount of energy to give each agent at the start of a run
    'i_energy': 0.5,
    # Constant for max population control (cost of surviving)
    'k': -1,  # ???
    # Constant for controlling dying of old age (T+M == Maximum lifespan)
    'T': 20,  # ???
    # Minimum lifespan
    'M': 10,  # ???
    # Minimum energy level to reproduce
    'p': 0.6,  # ???
    # Mutation "amplitude"
    'd': 0.5,
    # Whether to spawn children near parents or randomly
    'child_location': 'global',  # 'global'
    # Specify the type of movement allowed for the agents
    'movement': 'local-prob',  # 'local-prob'
    # Whether to print debug statements
    'debug': True,
}


def sigmoid(x):
    return 1 / (1 + math.e ** -x)


def agent_portrayal(agent):
    return {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": Color(rgb=(0, sigmoid(sum(agent.strategy)), 0)).get_hex(),
        "r": 0.5
    }


grid = CanvasGrid(
    agent_portrayal,
    params['size'],
    params['size'],
    500,
    500,
)
chart = ChartModule([
        {"Label": "n_agents",
         "Color": "Black"},
        {"Label": "n_friendlier",
         "Color": "Green"},
        {"Label": "n_aggressive",
         "Color": "Red"},
    ],
    data_collector_name='datacollector',
)


server = ModularServer(
    GTModel,
    [grid, chart],
    "Prisoners Dilemma Model",
    params,
)
server.port = 8522
server.launch()
