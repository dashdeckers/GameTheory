from model import GTModel

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule


params = {
    'size': 10,
    'n_agents': 5,
    'strategies': ['ALLC', 'ALLD', 'TFT'],
}


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5
    }

    if agent.strategy == 'ALLC':
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.5

    if agent.strategy == 'ALLD':
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.5

    if agent.strategy == 'TFT':
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.5

    return portrayal


grid = CanvasGrid(
    agent_portrayal,
    params['size'],
    params['size'],
    500,
    500,
)
chart = ChartModule([
        {"Label": "ALLC",
         "Color": "Green"},
        {"Label": "ALLD",
         "Color": "Red"},
        {"Label": "TFT",
         "Color": "Yellow"},
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
