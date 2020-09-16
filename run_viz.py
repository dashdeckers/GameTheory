from model import GTModel

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, PieChartModule


params = {
    'n_agents': 12,
    'n_food': 10,
    'strategies': ['Hawk', 'Dove'],
    'init_pop': 'Hawk invader',
}

chart = ChartModule([
        {"Label": "Doves",
         "Color": "Green"},
        {"Label": "Hawks",
         "Color": "Red"},
    ],
    data_collector_name='datacollector',
)
pie = PieChartModule([
        {"Label": "Doves",
         "Color": "Green"},
        {"Label": "Hawks",
         "Color": "Red"},
    ],
    data_collector_name='datacollector',
)


server = ModularServer(
    GTModel,
    [chart, pie],
    "Hawk Dove Game",
    params,
)
server.port = 8522
server.launch()
