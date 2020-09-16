from mesa import Agent


class GTAgent(Agent):
    def __init__(self, unique_id, model, strategy):
        super().__init__(unique_id, model)
        self.strategy = strategy
        self.food = 0
        self.memory = {}

    def get_action(self, opponent=None):
        if self.strategy == 'Hawk':
            return 'H'

        if self.strategy == 'Dove':
            return 'D'

    def step(self):
        # Go randomly through the food list and choose a free food,
        # where free means at most one other agent has chosen that food
        indices = list(range(self.model.n_food))
        self.random.shuffle(indices)

        for idx in indices:
            food_competitors = self.model.food_allocation[f'food_{idx}']
            if len(food_competitors) < 2:
                food_competitors.append(self)
                return
