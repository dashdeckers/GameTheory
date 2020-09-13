from agent import GTAgent

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


class GTModel(Model):
    def __init__(self, size, n_agents, strategies):
        self.grid = SingleGrid(size, size, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True

        # List of possible strategies
        self.strategies = strategies
        # Payoff matrix in the form (my_move, their_move) : my_reward
        self.payoff = {
            ('C', 'C'): 3,
            ('C', 'D'): 0,
            ('D', 'C'): 5,
            ('D', 'D'): 1,
        }

        # Add agents (one agent per cell)
        all_coords = [(x, y) for x in range(size) for y in range(size)]
        agent_coords = self.random.sample(all_coords, n_agents)

        for idx_id in range(n_agents):
            agent = GTAgent(idx_id, self, self.random.choice(self.strategies))
            self.schedule.add(agent)
            self.grid.place_agent(agent, agent_coords.pop())

        # Collect data
        self.datacollector = DataCollector(
            # we want the score of each agent, sorted by the agents strategy
            # average score? look this up
            # actually it would be enough just to know how many ALLC vs ALLD
            model_reporters={"Not Implemented": lambda x: 1}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        # evaluate fitness and place agents again?
        # agents with a higher score should "reproduce" more often right?
