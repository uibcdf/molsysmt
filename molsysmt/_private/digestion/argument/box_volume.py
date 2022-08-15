import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

def digest_box_volume(box_volume, caller=None):

    if caller=='molsysmt.basic.get.get':

        if isinstance(box_volume, bool):
            return box_volume

    raise ArgumentError('box_volume', value=box_volume, caller=caller, message=None)
