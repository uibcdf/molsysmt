from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_principal_axes_of_selection(principal_axes_of_selection, syntax="MolSysMT", caller=None):

    from .selection import digest_selection

    try:
        return digest_selection(principal_axes_of_selection, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('principal_axes_of_selection', value=principal_axes_of_selection, caller=caller, message=None)

