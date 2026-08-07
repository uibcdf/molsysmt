from ._chemical_state_query import digest_query_flag


def digest_reference_chemical_state_index(reference_chemical_state_index, caller=None):
    return digest_query_flag(
        'reference_chemical_state_index', reference_chemical_state_index, caller
    )
