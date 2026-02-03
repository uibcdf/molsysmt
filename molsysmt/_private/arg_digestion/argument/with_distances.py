from ...exceptions import ArgumentError

def digest_with_distances(with_distances, caller=None):

    if isinstance(with_distances, bool):
        return with_distances

    raise ArgumentError('with_distances', value=with_distances, caller=caller, message=None)

