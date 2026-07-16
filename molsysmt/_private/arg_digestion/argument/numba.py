from molsysmt._private.smonitor import ArgumentError


def digest_numba(numba, caller=None):
    if isinstance(numba, bool):
        return numba

    raise ArgumentError("numba", value=numba, caller=caller, message=None)
