# TODO: Find a way to reach the label of the model_reporter calling the func
# then we can a single function replace all these (DRY!)

def all_d_score(model):
    return sum([agent.score for agent in model.schedule.agents
                if agent.strategy == 'ALLD'])


def all_c_score(model):
    return sum([agent.score for agent in model.schedule.agents
                if agent.strategy == 'ALLC'])


def tft_score(model):
    return sum([agent.score for agent in model.schedule.agents
                if agent.strategy == 'TFT'])
