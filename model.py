from agent import GTAgent
from reporter_funcs import all_c_score, all_d_score, tft_score

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
        # Payoff matrix in the form (my_move, op_move) : my_reward
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
            # TODO: When reproduction is implemented, switch to a population
            # count of each strategy instead of total score per strategy
            model_reporters={"ALLC": all_c_score,
                             "ALLD": all_d_score,
                             "TFT": tft_score}
        )

    def step(self):
        for agent in self.schedule.agents:
            agent.acted = False

        self.datacollector.collect(self)
        self.schedule.step()

        # TODO: Evaluate fitness of each agent and have agents with a high
        # score reproduce (exact rules TBD)
