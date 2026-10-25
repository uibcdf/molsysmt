from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.vector_normalization import unit_vectors


def digest_direction(direction, caller=None):

    if caller is not None and caller.endswith("move_away"):
        if direction is None:
            return direction

    try:
        return unit_vectors(direction)
    except (TypeError, ValueError, OverflowError) as error:
        raise ArgumentError("direction", value=direction, caller=caller) from error
