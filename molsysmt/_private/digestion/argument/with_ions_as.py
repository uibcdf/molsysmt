from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_with_ions_as(with_ions_as, caller=None):

    if caller=='molsysmt.basic.view.view':
        if with_ions_as is None:
            return with_ions_as
        elif isinstance(with_ions_as, str):
            if with_ions_as in ['balls and sticks', 'balls', 'licorice']:
                return with_ions_as

    raise ArgumentError('with_ions_as', value=with_ions_as, caller=caller, message=None)

