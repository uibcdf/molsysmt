from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def has_waters(molecular_system):

    from molsysmt.basic import get

    output = False

    n_waters = get(molecular_system, element='system', n_waters=True)

    if n_waters>0:
        output = True

    return output

