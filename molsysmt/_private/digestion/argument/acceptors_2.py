from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_acceptors_2(acceptors_2, syntax="MolSysMT", caller=None):

    if acceptors_2 is None:
        return None

    from .acceptors import digest_acceptors

    try:
        return digest_acceptors(acceptors_2, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('acceptors_2', value=acceptors_2, caller=caller, message=None)

