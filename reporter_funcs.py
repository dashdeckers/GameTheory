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

    coop_actions = [
        a.NCactions for a in active_agents
        ]
    tot_actions = [
        a.Nactions for a in active_agents
        ]

    return sum(coop_actions) / sum(tot_actions)


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
    # Calculate the avg number of neighbors
    if not model.schedule.agents:
        return 0

    list_n_neighbors = [agent.n_neighbors for agent in model.schedule.agents]
    return sum(list_n_neighbors)/len(list_n_neighbors)


def perc_CC_interactions(model):
    # Calculate the percentage of the total number of cooperative actions
    number_coop_actions = sum(
        [a.NCactions for a in model.schedule.agents]
        )
    number_tot_actions = sum(
        [a.Nactions for a in model.schedule.agents]
        )
    
    if not number_tot_actions:
        return 0
    
    return number_coop_actions / number_tot_actions

def coop_per_neig(model):
    import scipy.optimize as optimize
    
    number_coop_actions = [
        a.NCactions for a in model.schedule.agents if a.n_neighbors != 0
    ]
    number_neighbors = [
        a.n_neighbors for a in model.schedule.agents if a.n_neighbors != 0
    ]
    
    if not number_neighbors:
        return 0
        
    def lin(x, a, b):
        return a*x + b
        
    return optimize.curve_fit(lin, number_neighbors, number_coop_actions)[0][0]


def coop_per_neig_intc(model):
    import scipy.optimize as optimize
    
    number_coop_actions = [
        a.NCactions for a in model.schedule.agents if a.n_neighbors != 0
    ]
    number_neighbors = [
        a.n_neighbors for a in model.schedule.agents if a.n_neighbors != 0
    ]
        
    if not number_neighbors:
        return 0
    
    def lin(x, a, b):
        return a*x + b
    
    return optimize.curve_fit(lin, number_neighbors, number_coop_actions)[0][1]

    