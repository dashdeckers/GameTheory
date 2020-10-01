from mesa import Agent
from pprint import pprint


class GTAgent(Agent):
    def __init__(self, unique_id, model, strategy, i_energy=0):
        super().__init__(unique_id, model)
        self.strategy = strategy
        self.total_energy = i_energy
        self.delta_energy = 0
        self.age = 0
        self.prev_interaction = None

    def move(self):
        # TODO: Implement the probability to move equals delta_energy (unclear)
        # My guess: determine the range [min, max] of delta_energy then convert
        # into a percentage and use that as an inverse probability of moving

        # If the last interaction was positive, don't move
        if self.delta_energy > 0:
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
        return 'D'

    def interact(self):
        # Reset delta energy
        self.delta_energy = 0
        # Get older
        self.age += 1

        # Find a neighbor that has not acted yet, if any
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=False,
            radius=1,
        )

        # Interact with each neighbor and sum energy changes
        interaction = None
        for opponent in neighbors:
            interaction = (self.action(), opponent.action())
            self.delta_energy += self.model.payoff[interaction]

        # Subtract the cost of surviving and update total energy
        self.delta_energy -= self.model.alpha()
        self.total_energy += self.delta_energy

        # Remember the last interaction (TODO: Seems arbitrary?)
        self.prev_interaction = interaction

    def step(self):
        #print('\n---------------------------')
        #print(f'Cost of Surviving: {self.model.alpha()}')
        self.interact()
        self.move()
        #pprint(vars(self))
