from molsysmt._private.exceptions import ArgumentError

def digest_n_neighbors(n_neighbors, caller=None):

    if n_neighbors is None:
        return None

    if isinstance(n_neighbors, int):
        return n_neighbors

    raise ArgumentError('n_neighbors', value=n_neighbors, caller=caller, message=None)

