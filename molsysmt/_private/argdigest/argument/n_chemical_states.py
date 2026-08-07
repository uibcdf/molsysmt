from ._chemical_state_query import digest_query_flag


def digest_n_chemical_states(n_chemical_states, caller=None):
    return digest_query_flag('n_chemical_states', n_chemical_states, caller)
