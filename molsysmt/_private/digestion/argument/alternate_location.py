import numpy as np
from ...exceptions import ArgumentError

def digest_alternate_location(alternate_location, caller=None):

    if caller=='molsysmt.basic.get.get':

        if isinstance(alternate_location, bool):
            return alternate_location

    raise ArgumentError('alternate_location', value=alternate_location, caller=caller, message=None)
