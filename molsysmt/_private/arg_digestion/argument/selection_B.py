from molsysmt.exceptions import ArgumentError
import numpy as np

def digest_selection_B(selection_B, syntax="MolSysMT", caller=None):

    from .selection import arg_digest_selection

    try:
        return digest_selection(selection_B, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('selection_B', value=selection_B, caller=caller, message=None)

