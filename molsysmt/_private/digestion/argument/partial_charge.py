import numpy as np
from ...exceptions import ArgumentError

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_partial_charge(partial_charge, caller=None):

    if caller.endswith(functions_with_boolean):
        if isinstance(partial_charge, bool):
            return partial_charge
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return partial_charge

    raise ArgumentError('partial_charge', value=partial_charge, caller=caller, message=None)
