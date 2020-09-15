from mesa import Agent


class GTAgent(Agent):
    def __init__(self, unique_id, model, strategy):
        super().__init__(unique_id, model)
        self.strategy = strategy
        self.score = 0
        self.acted = False
        self.memory = {}

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

        # TODO: Maybe move next to a cell occopied by an agent using
        # the same strategy? Similar animals tend to group together
        # UPDATE: That will skew results, not recommended

    def get_action(self, opponent):
        if self.strategy == 'ALLC':
            return 'C'

        if self.strategy == 'ALLD':
            return 'D'

        if self.strategy == 'TFT':
            # First be nice
            if opponent.unique_id not in self.memory:
                return 'C'

            # Then be retaliatory but forgiving
            if self.memory[opponent.unique_id] == 'D':
                return 'D'
            if self.memory[opponent.unique_id] == 'C':
                return 'C'

    def interact(self):
        # Find a neighbor that has not acted yet, if any
        free_neighbors = [agent for agent in self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=1,
        ) if not agent.acted]

        if not free_neighbors or self.acted:
            return

        # Choose an opponent and interact with them
        opponent = self.random.choice(free_neighbors)

        my_action = self.get_action(opponent)
        op_action = opponent.get_action(self)

        self.score += self.model.payoff[(my_action, op_action)]
        opponent.score += self.model.payoff[(op_action, my_action)]

        self.acted = True
        opponent.acted = True

        self.memory[opponent.unique_id] = op_action
        opponent.memory[self.unique_id] = my_action

    def step(self):
        self.move()
        self.interact()
