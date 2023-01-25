import numpy as np
from ...exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_formal_charge(formal_charge, caller=None):

    if caller.endswith(functions_with_boolean):
        if isinstance(formal_charge, bool):
            return formal_charge

    raise ArgumentError('formal_charge', value=formal_charge, caller=caller, message=None)
