import numpy as np
from ...exceptions import ArgumentError

def digest_formal_charge(formal_charge, caller=None):

    if caller=='molsysmt.basic.get.get':

        if isinstance(formal_charge, bool):
            return formal_charge

    raise ArgumentError('formal_charge', value=formal_charge, caller=caller, message=None)
