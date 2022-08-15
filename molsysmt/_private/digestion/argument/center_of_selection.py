from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_center_of_selection(center_of_selection, syntax="MolSysMT", caller=None):

    from .selection import digest_selection

    try:
        return digest_selection(center_of_selection, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('center_of_selection', value=center_of_selection, caller=caller, message=None)

