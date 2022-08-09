from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import puw

def digest_standardize(standardize, caller=None):

    if caller=='molsysmt.basic.view.view':
        if isinstance(standardize, bool):
            return standardize

    raise ArgumentError('standardize', value=standardize, caller=caller, message=None)

