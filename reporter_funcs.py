
def total_n_agents(model):
    return len(model.schedule.agents)


def avg_agent_age(model):
    return (
        sum([agent.age for agent in model.schedule.agents])
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
        a for a in model.schedule.agents if a.prev_interaction is not None
    ]

    if not active_agents:
        return 0

    non_coop_agents = [
        a for a in active_agents if a.prev_interaction[0] == 'C'
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

def nneighbor_measure(model):
    #Calculate the average number of neighbors div by the total number of agents
    #Is a measure of how clustered agents are
    #0.02 seems to be the threshold value for solid clusters.
    list_nneighbors = [agent.nneighbors for agent in model.schedule.agents]
    return sum(list_nneighbors)/len(list_nneighbors)**2