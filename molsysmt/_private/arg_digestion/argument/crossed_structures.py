from ...exceptions import ArgumentError

def digest_crossed_structures(crossed_structures, caller=None):

    if caller=='molsysmt.structure.get_distances.get_distances':
        if isinstance(crossed_structures, bool):
            return crossed_structures

    raise ArgumentError('crossed_structures', value=crossed_structures, caller=caller, message=None)

