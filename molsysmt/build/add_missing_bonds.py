from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest()
def add_missing_bonds(molecular_system, threshold='2 angstroms', selection='all',
                      structure_indices=0, syntax='MolSysMT', engine='MolSysMT',
                      in_place=True, skip_digestion=False):
    """
    To be written soon...
    """

    if engine=='MolSysMT':

        from molsysmt.build import get_missing_bonds
        from molsysmt.build import add_bonds

        bonds = get_missing_bonds(molecular_system, threshold=threshold, selection=selection,
                                 structure_indices=structure_indices, syntax=syntax,
                                 skip_digestion=True)

        return add_bonds(molecular_system, bonds, in_place=in_place, skip_digestion=True)

    elif engine=="ParmEd":

        raise NotImplementedError

    elif engine=="pytraj":

        raise NotImplementedError

    else:

        raise NotImplementedError

    raise NotImplementedError

