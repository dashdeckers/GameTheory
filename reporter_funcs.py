def total_n_agents(model):
    return len(model.schedule.agents)


def n_friendlier(model):
    return len([agent for agent in model.schedule.agents
                if sum(agent.strategy)/4 >= 0.5])


def n_aggressive(model):
    return len([agent for agent in model.schedule.agents
                if sum(agent.strategy)/4 < 0.5])
