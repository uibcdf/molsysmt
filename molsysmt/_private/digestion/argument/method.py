import numpy as np
from ...exceptions import ArgumentError
from ...variables import is_all

def digest_method(method, caller=None):

    if caller=='molsysmt.structure.align.align':
        if isinstance(method, str):
            return method
    elif caller=='molsysmt.physchem.get_mass.get_mass':
        if isinstance(method, str):
            if method in ['OpenMM', 'physical']:
                return method


    return ArgumentError('method', value=method, caller=caller, message=None)

