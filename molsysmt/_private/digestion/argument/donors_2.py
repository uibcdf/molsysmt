from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_donors_2(donors_2, syntax="MolSysMT", caller=None):

    if donors_2 is None:
        return None

    from .donors import digest_donors

    try:
        return digest_donors(donors_2, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('donors_2', value=donors_2, caller=caller, message=None)

