from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_concatenate_structures(concatenate_structures, caller=None):

    if caller=='molsysmt.basic.view.view':
        if isinstance(concatenate_structures, bool):
            return concatenate_structures

    raise ArgumentError('concatenate_structures', value=concatenate_structures, caller=caller, message=None)

