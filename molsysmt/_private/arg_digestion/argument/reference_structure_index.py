from ...exceptions import ArgumentError
import numpy as np

def digest_reference_structure_index(reference_structure_index, caller=None):

    if isinstance(reference_structure_index, (int, np.int64, np.int32)):
        return reference_structure_index

    raise ArgumentError('reference_structure_index', value=reference_structure_index, caller=caller, message=None)

