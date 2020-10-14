from mesa import Agent
from pprint import pprint


class GTAgent(Agent):
    def __init__(self, unique_id, group_id, model, strategy, i_energy):
        super().__init__(unique_id, model)
        self.group_id = group_id
        self.strategy = strategy
        self.total_energy = i_energy
        self.delta_energy = 0
        self.age = 0
        self.prev_interaction = None
        self.n_neighbors = 0

    def move(self):
        if self.model.movement == 'none':
            return

        if self.model.movement == 'global':
            self.model.grid.move_agent(
                self, self.random.choice(sorted(self.model.grid.empties))
            )

        if self.model.movement == 'local-free':
            # If the last interaction was positive, don't move
            if self.delta_energy >= 1:
                return

        if self.model.movement == 'local-prob':
            # Determine whether to move based on delta_energy
            # alpha is in [-1, 15) for k=-1  (with N from 0-400 on a 20x20 map)
            # If we take N=200 as the max population, we get alpha=7
            # The worst possible payoff per round is 4*-3=-12
            prob_moving = 0
            if self.delta_energy < 0:
                prob_moving = self.delta_energy / -12

            if self.random.random() < prob_moving:
                return

        # Van Neumann neighborhood
        possible_steps = [cell for cell in self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False,
            radius=1,
        ) if self.model.grid.is_cell_empty(cell)]

        # If we can't move, don't move
        if not possible_steps:
            return

        # Move to random free position
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def action(self):
        # Initial move should be random to remove bias
        if not self.prev_interaction:
            if self.random.random() < 0.5:
                return 'C'
            else:
                return 'D'

        # Strategy: P(C|prev), where prev in [CC, CD, DC, DD]
        # Represented by a dictionary: {prev_interaction: P(C)}
        prob_dict = {
            interaction: p for interaction, p in
            zip([('C', 'C'), ('C', 'D'), ('D', 'C'), ('D', 'D')],
                self.strategy)
        }

        if self.random.random() < prob_dict[self.prev_interaction]:
            return 'C'
        else:
            return 'D'

    def interact(self):
        # Reset delta energy
        self.delta_energy = 0
        # Get older
        self.age += 1

        # Get neighbors
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=False,
            radius=1,
        )
        # Update number of neigbors
        self.n_neighbors = len(neighbors)

        # Interact with each neighbor and sum energy changes
        interaction = None
        for other in neighbors:
            # If the neighbor is in the same group, no need for a PD game
            if self.group_id is not None and other.group_id == self.group_id:
                pass
            else:
                interaction = (self.action(), other.action())
                self.delta_energy += self.model.payoff[interaction]

        # Subtract the cost of surviving and update total energy
        self.delta_energy -= self.model.alpha()
        self.total_energy += self.delta_energy

        # Update the last interaction, if there was one
        if interaction:
            self.prev_interaction = interaction

    def step(self):
        self.interact()
        self.move()

        if self.model.debug:
            print('\n---------------------------')
            print(f'Cost of Surviving: {self.model.alpha()}')
            print(f'Agent strategy: {self.model.check_strategy(self)}')
            pprint(vars(self))
