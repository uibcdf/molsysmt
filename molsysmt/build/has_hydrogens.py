from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest()
def has_hydrogens(molecular_system, selection='all', syntax='MolSysMT', skip_digestion=False):

    from molsysmt.basic import get

    mask = get(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
    n_Hs = get(molecular_system, selection='atom_type=="H"', mask=mask, skip_digestion=True, n_atoms=True)

    return n_Hs>0
