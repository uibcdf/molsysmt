import numpy as np
from ...exceptions import ArgumentError

def digest_partial_charge(partial_charge, caller=None):

    if caller=='molsysmt.basic.get.get':

        if isinstance(partial_charge, bool):
            return partial_charge

    raise ArgumentError('partial_charge', value=partial_charge, caller=caller, message=None)
