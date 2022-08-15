from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_selection_A(selection_A, syntax="MolSysMT", caller=None):

    from .selection import digest_selection

    try:
        return digest_selection(selection_A, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('selection_A', value=selection_A, caller=caller, message=None)
