from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_wrap(wrap, caller=None):

    if caller=='molsysmt.basic.convert.convert':
        if isinstance(wrap, str):
            if wrap.lower() in ['mic', 'pbc', 'unwrap']:
                return wrap.lower()

    raise ArgumentError('wrap', value=wrap, caller=caller, message=None)

