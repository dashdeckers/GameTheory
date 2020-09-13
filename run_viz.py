from model import GTModel

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


params = {
    'size': 10,
    'n_agents': 5,
    'strategies': ['ALLC', 'ALLD'],
}


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5
    }

    if agent.strategy == 'ALLD':
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
    elif agent.strategy == 'ALLC':
        portrayal["Color"] = "green"
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

server = ModularServer(
    GTModel,
    [grid],
    "Prisoners Dilemma Model",
    params,
)
server.port = 8522
server.launch()
