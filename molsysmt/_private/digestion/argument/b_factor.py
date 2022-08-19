import numpy as np
from ...exceptions import ArgumentError

def digest_b_factor(b_factor, caller=None):

    if caller=='molsysmt.basic.get.get':

        if isinstance(b_factor, bool):
            return b_factor

    raise ArgumentError('b_factor', value=b_factor, caller=caller, message=None)
