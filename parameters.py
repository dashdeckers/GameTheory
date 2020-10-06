params = {
    # The map size
    'size': 20,  # 20
    # Initial number of agents to place at the start of a run
    'i_n_agents': 60,  # 60  (supposed to naturally grow to avg 100)
    # Initial strategy for every agent at the start of a run
    'i_strategy': [0.5, 0.5, 0.5, 0.5],  # [0.5] * 4
    # Initial amount of energy to give each agent at the start of a run
    'i_energy': 0.5,  # ???
    # Constant for max population control (cost of surviving)
    'k': -2.5,
    # Constant for controlling dying of old age (T+M == Maximum lifespan)
    'T': 10,
    # Minimum lifespan
    'M': 5,
    # Minimum energy level to reproduce
    'p': 1,
    # Mutation 'amplitude'
    'd': 0.1,
    # Whether to spawn children near parents or randomly
    'child_location': 'global',
    # Specify the type of movement allowed for the agents
    'movement': 'local-prob',
    # Whether to print debug statements
    'debug': False,
    # Strategies to count
    'strategies_to_count': {
            # 'RANDOM':   [.5, .5, .5, .5],
            'ALLC':     [1, 1, 1, 1],
            'ALLD':     [0, 0, 0, 0],
            'TFT':      [1, 0, 1, 0],
            'GRIM':     [1, 0, 0, 0],
            'PAVLOV':   [1, 0, 0, 1],
            'GUILTY':   [0, 0, 1, 0],
            'BRAT':     [0, 1, 0, 1],
            'ISSUES':   [0, 1, 1, 1],
            'DIPLOMAT': [1, 0, 1, 1],
            'NEGPAV':   [0, 1, 1, 0],
            'PSYCHO':   [1, 1, 0, 1],
            'REPEATER': [1, 1, 0, 0],
            'SWITCHER': [0, 0, 1, 1],
            'CRYBABY':  [0, 1, 0, 0],
            '0001':     [0, 0, 0, 1],
            '1110':     [1, 1, 1, 0],
    },

    # Count tolerance
    'count_tolerance': 0.3,
}
