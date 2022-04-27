from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def has_cosolutes(molecular_system):

    from molsysmt.basic import get

    output = False

    n_cosolutes = get(molecular_system, element='system', n_cosolutes=True)

    if n_cosolutes>0:
        output = True

    return output

