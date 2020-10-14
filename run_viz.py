import math

from model import GTModel
from parameters import params, strategy_colors

from colour import Color
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, PieChartModule


def agent_portrayal(agent):
    """Visualize the general niceness of an agent by summing the strategy
    values and squashing it between [0,1] using a sigmoid. The 'green'
    intensity then corresponds to the niceness."""
    def sigmoid(x):
        return 1 / (1 + math.e ** -x)

    if agent.group_id is None:
        agent_color = Color(rgb=(0, sigmoid(4 - sum(agent.strategy)), 0)).get_hex()
    else:
        agent_color = strategy_colors[agent.group_id]

    return {
        'Shape': 'circle',
        'Filled': 'true',
        'Layer': 0,
        'Color': agent_color,
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
    {'Label': 'avg_agent_age',
     'Color': 'Gray'},
])
perc_chart = ChartModule([
    {'Label': 'perc_cooperative_actions',
     'Color': 'Green'},
])
strategy_chart = ChartModule([
    {'Label': label, 'Color': color}
    for label, color in
    zip(params['strategies_to_count'].keys(), strategy_colors)
])
clustering_chart = ChartModule([
    {'Label': 'n_neighbors',
     'Color': 'Red'},
])


server = ModularServer(
    GTModel,
    [grid, clustering_chart, total_chart, perc_chart, strategy_chart],
    'Prisoners Dilemma Model',
    params,
)
server.port = 8522
server.launch()
