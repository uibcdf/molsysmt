from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest()
def has_hydrogens(molecular_system, selection='all', syntax='MolSysMT', skip_digestion=False):
    """Check whether a molecular system (or selection) contains hydrogen atoms."""

    from molsysmt.basic import get, select

    if is_all(selection):
        n_Hs = get(molecular_system, selection='atom_type=="H"', n_atoms=True, skip_digestion=True)
    else:
        mask = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
        n_Hs = get(molecular_system, selection='atom_type=="H"', mask=mask, n_atoms=True, skip_digestion=True)

    return n_Hs>0
