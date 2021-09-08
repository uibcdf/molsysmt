from molsysmt._private_tools.exceptions import *

def has_hydrogens(molecular_system):

    from molsysmt.multitool import get

    output = False

    n_hydrogens = get(molecular_system, target='atom', selection='atom_type=="H"', n_atoms=True)

    if n_hydrogens>0:
        output = True

    return output

