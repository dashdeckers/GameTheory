from mesa import Agent


class GTAgent(Agent):
    def __init__(self, unique_id, model, strategy):
        super().__init__(unique_id, model)
        self.strategy = strategy
        self.score = 0

    def move(self):
        # Move to random new (empty!) location in a 9 cell radius
        possible_steps = [cell for cell in self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True,
            radius=1,
        ) if self.model.grid.is_cell_empty(cell)]

        if not possible_steps:
            return

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def interact(self):
        # Interact with a neighbor, if any, and recieve a score
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=1,
        )

        if not neighbors:
            return

        chosen_neighbor = self.random.choice(neighbors)

        # illustrative code
        config = (self.strategy[-1], chosen_neighbor.strategy[-1])
        print(f'Interaction: {config}, Reward: {self.model.payoff[config]}')

        # does each agent keep a dictionary of past encounters?

        # an encounter is a two way interaction, so it can happen that in the
        # same agent loop a single agent has two or more interactions. how to
        # handle this?
        pass

    def step(self):
        self.move()
        self.interact()
