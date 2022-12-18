from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_standard(standard, caller=None):

    if caller=='molsysmt.basic.view.view':
        if isinstance(standard, bool):
            return standard

    raise ArgumentError('standard', value=standard, caller=caller, message=None)

