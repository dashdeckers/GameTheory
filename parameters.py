from itertools import product

# In comments: The values from the paper
params = {
    # The map size
    'size': 17,  # 20
    # Initial number of agents to place at the start of a run
    'i_n_agents': 60,  # 60  (supposed to naturally grow to avg 100)
    # Initial amount of energy to give each agent at the start of a run
    'i_energy': 1,  # ???
    # Initial strategy for every agent at the start of a run
    'i_strategy': [0.5, 0.5, 0.5, 0.5],  # [0.5] * 4
    # Constant for max population control (cost of surviving)
    'k': -3,  # ??? (-3 gives alpha=0 for 100 agents)
    # For 20x20 alpha=k + 4*DC*CC*N/400
    # N=100 -> a=k+DC*CC, DC*CC = 3 -> k=-3 for alpha=0 at 100 agents
    # Constant for controlling dying of old age (T+M == Maximum lifespan)
    'T': 50,  # ???
    # Minimum lifespan
    'M': 100,  # ???
    # Minimum energy level to reproduce
    'p': 3,  # ???
    # Mutation 'amplitude'
    'd': 0.2,  # 0.1
    # The minimum total_energy needed for an agent to survive
    'death_threshold': -3,  # 0

    # Whether to spawn children near parents or randomly
    # Must be in ['local' or 'global']
    'child_location': 'local',  # 'global'
    # Specify the type of movement allowed for the agents
    # Must be in ['local-prob', 'local-free', 'global', 'none']
    'movement': 'local-prob',  # 'local-prob'
    # Specify how agents mutate
    # Must be in ['fixed', 'stochastic', 'gaussian_sentimental']
    'mutation_type': 'stochastic',  # 'stochastic'
    # The number of groups to create
    # Must be an integer >0 or None
    'n_groups': None,  # None

    # Strategies to count
    # P(C|S), where S in [CC, CD, DC, DD]
    'strategies_to_count': {
        str(strategy): list(strategy) for strategy in
        product(*[[0, 1] for _ in range(4)])
    },
    #         'ALLC':     [1, 1, 1, 1],
    #         'ALLD':     [0, 0, 0, 0],
    #         'TFT':      [1, 0, 1, 0],
    #         'GRIM':     [1, 0, 0, 0],
    #         'PAVLOV':   [1, 0, 0, 1],
    #         'GUILTY':   [0, 0, 1, 0],
    #         'BRAT':     [0, 1, 0, 1],
    #         'ISSUES':   [0, 1, 1, 1],
    #         'DIPLOMAT': [1, 0, 1, 1],
    #         'NEGPAV':   [0, 1, 1, 0],
    #         'PSYCHO':   [1, 1, 0, 1],
    #         'REPEATER': [1, 1, 0, 0],
    #         'SWITCHER': [0, 0, 1, 1],
    #         'CRYBABY':  [0, 1, 0, 0],
    #         '0001':     [0, 0, 0, 1],
    #         '1110':     [1, 1, 1, 0],
    # },
    # Count tolerance
    'count_tolerance': 0.3,

    # Whether to print debug statements
    'debug': False,  # 'True' or 'False'
}

strategy_colors = [
    'Green', 'Red', 'Yellow', 'Orange', 'Blue',
    'Aqua', 'Black', 'Fuchsia', 'Gray', 'Lime',
    'Maroon', 'Navy', 'Olive', 'Purple', 'Silver',
    'Teal', 'White',
]

# Batch run parameters
run_name = 'p_sweep_memory'
iterations = 50
max_steps = 5000

# Needs at least one item even if its a single value: [60]
var_params = {
    'p': [1, 2, 3, 4],
    # 'death_threshold': [0, -1, -5],
}
