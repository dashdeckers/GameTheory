from agent import GTAgent
from reporter_funcs import total_n_agents, n_aggressive, n_friendlier

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


class GTModel(Model):
    def __init__(self, size, i_n_agents, i_strategy, i_energy, k, T, M, p, d):
    def __init__(self, debug, size, i_n_agents, i_strategy, i_energy,
        self.grid = SingleGrid(size, size, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.debug = debug
        self.size = size
        self.agent_idx = 0

        # Payoff matrix in the form (my_move, op_move) : my_reward
        self.payoff = {
            ('C', 'C'): 1,
            ('C', 'D'): -3,
            ('D', 'C'): 3,
            ('D', 'D'): -1,
        }
        # Constant for max population control (cost of surviving)
        self.k = k
        # Constant for controlling dying of old age
        self.M = M
        # Minimum lifespan
        self.T = T
        # Minimum energy level to reproduce
        self.p = p
        # Mutation "amplitude"
        self.d = d
        # Whether to spawn children near parents or randomly
        self.child_location = child_location
        # Specify the type of movement allowed for the agents
        self.movement = movement

        # Add agents (one agent per cell)
        all_coords = [(x, y) for x in range(size) for y in range(size)]
        agent_coords = self.random.sample(all_coords, i_n_agents)

        for _ in range(i_n_agents):
            agent = GTAgent(self.agent_idx, self, i_strategy.copy(), i_energy)
            self.agent_idx += 1
            self.schedule.add(agent)
            self.grid.place_agent(agent, agent_coords.pop())

        # Collect data
        self.datacollector = DataCollector(model_reporters={
            'n_agents': total_n_agents,
            'n_friendlier': n_friendlier,
            'n_aggressive': n_aggressive,
        })

    def alpha(self):
        # Return the cost of surviving, alpha
        DC = self.payoff[('D', 'C')]
        CC = self.payoff[('C', 'C')]
        N = len(self.schedule.agents)

        return self.k + 4 * (DC + CC) * N / (self.size * self.size)

    def time_to_die(self, agent):
        # There is a chance every iteration to die of old age: (A - T) / M
        # There is a 100% to die if the agents total energy reaches 0
        prob_too_old = (agent.age - self.T) / self.M
        return agent.total_energy < 0 or self.random.random() < prob_too_old

    def get_child_location(self, agent):
        if self.child_location == 'global':
            return self.random.choice(sorted(self.grid.empties))

        elif self.child_location == 'local':
            # Iterate over the radius, starting at 1 to find empty cells
            for rad in range(1, int(self.size/2)):
                possible_steps = [cell for cell in self.grid.get_neighborhood(
                    agent.pos,
                    moore=False,
                    include_center=False,
                    radius=rad,
                ) if self.grid.is_cell_empty(cell)]

                if possible_steps:
                    return self.random.choice(possible_steps)

            # If no free cells in radius size/2 pick a random empty cell
            return self.random.choice(sorted(self.grid.empties))

    def maybe_mutate(self, strategy):
        # Copy the damn list
        new_strategy = strategy.copy()
        # There is a 20% chance of mutation
        if self.random.random() < 0.2:
            # Each Pi is mutated uniformly by [-d, d]
            for i in range(4):
                mutation = self.random.uniform(-self.d, self.d)
                new_val = new_strategy[i] + mutation
                # Keep probabilities in [0, 1]
                new_val = 0 if new_val < 0 else 1 if new_val > 1 else new_val
                new_strategy[i] = new_val

        return new_strategy

    def maybe_reproduce(self, agent):
        # If we have the energy to reproduce, do so
        if agent.total_energy >= self.p:
            # Create the child
            new_strategy = self.maybe_mutate(agent.strategy)
            child = GTAgent(self.agent_idx, self, new_strategy)
            self.agent_idx += 1

            # Set parent and child energy levels to p/2
            child.total_energy = self.p / 2
            agent.total_energy = self.p / 2

            # Place child (Remove agent argument for global child placement)
            self.schedule.add(child)
            self.grid.place_agent(child, self.get_child_location(agent))

    def step(self):
        if self.debug:
            print('\n\n==================================================')
            print('==================================================')
            print('==================================================')

        # First collect data
        self.datacollector.collect(self)

        # Then check for dead agents and for new agents
        for agent in self.schedule.agent_buffer(shuffled=True):
            # First check if dead
            if self.time_to_die(agent):
                self.grid.remove_agent(agent)
                self.schedule.remove(agent)

            # Otherwise check if can reproduce
            else:
                self.maybe_reproduce(agent)
        # Finally, step each agent
        self.schedule.step()
