import numpy as np
from ...exceptions import ArgumentError
from ...variables import is_all

_methods_align = [
        'sequence alignment and least rmsd fit',
        ]

def digest_method(method, caller=None):

    if caller=='molsysmt.structure.align.align':
        if isinstance(method, str):
            return method

    return ArgumentError('method', value=method, caller=caller, message=None)

