import numpy as np
from ...exceptions import ArgumentError
from ...variables import is_all


def digest_reference_structure_index(reference_structure_index, caller=None):

    if caller=='molsysmt.structure.align.align':
        if isinstance(reference_structure_index, int):
            return reference_structure_index

    return ArgumentError('reference_structure_index', value=reference_structure_index, caller=caller, message=None)

