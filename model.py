from agent import GTAgent
from reporter_funcs import hawk_count, dove_count

from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class GTModel(Model):
    def __init__(self, n_agents, n_food, strategies, init_pop='Dove'):
        self.schedule = RandomActivation(self)
        self.running = True

        # List of possible strategies
        self.strategies = strategies
        self.init_pop = init_pop
        self.n_agents = n_agents
        self.n_food = n_food

        self.payoff = {
            ('H', 'H'): 0,
            ('H', 'D'): 1.5,
            ('D', 'H'): 0.5,
            ('D', 'D'): 1,
        }

        # Add agents
        for strategy in self.get_strategy_list():
            agent = GTAgent(self.get_idx(), self, strategy)
            self.schedule.add(agent)

        # Add food (just a dictionary of lists, no actual Agent objects)
        self.food_allocation = {f'food_{i}': [] for i in range(self.n_food)}

        # Collect data
        self.datacollector = DataCollector(
            model_reporters={"Hawks": hawk_count,
                             "Doves": dove_count}
        )

    def get_idx(self):
        # Get a unique random hash because counting indices is annoying
        return hash(self.random.random())

    def get_strategy_list(self):
        # Get the initial distribution of strategies.
        if self.init_pop == 'random':
            # Random initial strategies
            return [self.random.choice(self.strategies)
                    for _ in range(self.n_agents)]

        if self.init_pop == 'Hawk invader':
            # A single Hawk among Doves
            return ['Dove'] * (self.n_agents - 1) + ['Hawk']

        if self.init_pop == 'Dove invader':
            # A single Dove among Hawks
            return ['Hawk'] * (self.n_agents - 1) + ['Dove']

        if self.init_pop in self.strategies:
            # All the same strategy (provide a single strategy)
            return [self.init_pop] * self.n_agents

        if len(self.init_pop) == self.n_agents:
            # Custom distribution (provide a list of strategies)
            return self.init_pop

    def get_offspring(self, food, strategy):
        # 100% replication chance
        if food == 2:
            return [
                GTAgent(self.get_idx(), self, strategy),
                GTAgent(self.get_idx(), self, strategy),
            ]

        # 50% replication chance
        if food == 1.5:
            if self.random.random() < 0.5:
                return [
                    GTAgent(self.get_idx(), self, strategy),
                    GTAgent(self.get_idx(), self, strategy),
                ]
            else:
                return [GTAgent(self.get_idx(), self, strategy)]

        # 100% survival chance
        if food == 1:
            return [GTAgent(self.get_idx(), self, strategy)]

        # 50% survival chance
        if food == 0.5:
            if self.random.random() < 0.5:
                return [GTAgent(self.get_idx(), self, strategy)]
            else:
                return []

        # 0% survival chance
        if food == 0:
            return []

    def reproduce(self):
        # Determine the new generation of agents
        for agent in self.schedule.agent_buffer():
            for new_agent in self.get_offspring(agent.food, agent.strategy):
                self.schedule.add(new_agent)
            self.schedule.remove(agent)

    def compete(self):
        # Determine who gets which food
        for food, competitors in self.food_allocation.items():
            if len(competitors) == 1:
                competitors[0].food = 2

            if len(competitors) == 2:
                [agent1, agent2] = competitors

                move1 = agent1.get_action()
                move2 = agent2.get_action()

                agent1.food += self.payoff[(move1, move2)]
                agent2.food += self.payoff[(move2, move1)]

        self.food_allocation = {f'food_{i}': [] for i in range(self.n_food)}

    def step(self):
        self.schedule.step()
        self.compete()
        self.reproduce()

        self.datacollector.collect(self)
