from ._chemical_state_query import digest_query_flag


def digest_connectivity_completeness(connectivity_completeness, caller=None):
    return digest_query_flag('connectivity_completeness', connectivity_completeness, caller)
