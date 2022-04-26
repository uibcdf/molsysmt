from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def has_hydrogens(molecular_system):

    from molsysmt.basic.get import get

    output = False

    n_hydrogens = get(molecular_system, target='atom', selection='atom_type=="H"', n_atoms=True)

    if n_hydrogens>0:
        output = True

    return output

