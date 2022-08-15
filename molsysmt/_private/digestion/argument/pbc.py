from ...exceptions import ArgumentError

def digest_pbc(pbc, caller=None):

    if isinstance(pbc, bool):
        return pbc

    raise ArgumentError('pbc', value=pbc, caller=caller, message=None)

