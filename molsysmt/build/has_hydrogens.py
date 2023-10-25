from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest()
def has_hydrogens(molecular_system, selection='all', syntax='MolSysMT'):

    from molsysmt.basic import get

    mask = get(molecular_system, selection=selection, syntax=syntax)
    n_Hs = get(molecular_system, selection='atom_type=="H"', mask=mask, n_atoms=True)

    return n_Hs>0
