from ._chemical_state_query import digest_query_flag


def digest_chemical_state_index(chemical_state_index, caller=None):
    return digest_query_flag('chemical_state_index', chemical_state_index, caller)
