def total_n_agents(model):
    return len(model.schedule.agents)


def avg_agent_age(model):
    if not model.schedule.agents:
        return 0

    return (
        sum([agent.age for agent in model.schedule.agents])
        / len(model.schedule.agents)
    )

def avg_delta_energy(model):
    if not model.schedule.agents:
        return 0

    return (
        sum([agent.delta_energy for agent in model.schedule.agents])
        / len(model.schedule.agents)
    )

def n_friendlier(model):
    return len([agent for agent in model.schedule.agents
                if sum(agent.strategy)/4 >= 0.5])


def n_aggressive(model):
    return len([agent for agent in model.schedule.agents
                if sum(agent.strategy)/4 < 0.5])


def perc_cooperative_actions(model):
    active_agents = [
        a for a in model.schedule.agents if a.rece_interaction is not None
    ]

    if not active_agents:
        return 0

    non_coop_agents = [
        a for a in active_agents if a.rece_interaction[0] == 'C'
    ]  # Non coop agents name but returning agents who did coop?

    return len(non_coop_agents) / len(active_agents)


def get_strategies(model):
    return [agent.strategy for agent in model.schedule.agents]


def strategy_counter_factory(strategy, tol):
    def strategy_counter(model):
        return len([
            a for a in model.schedule.agents
            if all(
                strategy[i] - tol < a.strategy[i] < strategy[i] + tol
                for i in range(4))
        ])
    return strategy_counter


def n_neighbor_measure(model):
    # Calculate the avg number of neighbors div by the total number of agents
    # Is a measure of how clustered agents are
    # 0.02 seems to be the threshold value for solid clusters.
    if not model.schedule.agents:
        return 0

    list_n_neighbors = [agent.n_neighbors for agent in model.schedule.agents]
    return sum(list_n_neighbors)/len(list_n_neighbors)
