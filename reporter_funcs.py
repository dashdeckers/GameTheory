def hawk_count(model):
    return len([agent for agent in model.schedule.agents
                if agent.strategy == 'Hawk'])


def dove_count(model):
    return len([agent for agent in model.schedule.agents
                if agent.strategy == 'Dove'])
