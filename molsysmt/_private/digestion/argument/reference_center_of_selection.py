from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_reference_center_of_selection(reference_center_of_selection, syntax="MolSysMT", caller=None):

    from .selection import digest_selection

    try:
        return digest_selection(reference_center_of_selection, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('reference_center_of_selection', value=center_of_selection, caller=caller, message=None)

