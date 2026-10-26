import numpy as np
from argdigest.core.caller import caller_is_one_of

from molsysmt._private.smonitor import ArgumentError


def digest_vector(vector, caller=None):

    if caller_is_one_of(caller, {"molsysmt.structure.flip.flip"}):
        from molsysmt._private.vector_normalization import unit_vectors

        normal = [0.0, 0.0, 1.0] if vector is None else vector
        try:
            normalized = unit_vectors(normal)
            if np.shape(normal) != (3,):
                raise ValueError("A plane normal must have shape (3,).")
            return normalized[0]
        except (TypeError, ValueError, OverflowError) as error:
            raise ArgumentError("vector", value=vector, caller=caller) from error

    if isinstance(vector, (list, tuple)):
        vector = np.array(vector, dtype=np.float64)

    if isinstance(vector, np.ndarray):
        if (len(vector.shape) == 1) and (vector.shape[0] == 3):
            vector = vector.astype(np.float64)
            return vector

    raise ArgumentError("vector", value=vector, caller=caller, message=None)
