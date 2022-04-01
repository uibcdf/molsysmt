# ==================================================
# Methods to remove elements from a molecular system
# ==================================================

"""
Remove waters
==============
Methods to remove atoms from a molecular model.
"""

from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def remove_waters (molecular_system, selection="all", include_selection=None,
        exclude_selection=None, syntaxis="MolSysMT", check=True):

    from molsysmt.basic import select, remove, is_molecular_system

    if check:

        if not is_molecular_system(molecular_system):
            raise NeedsSingleMolecularSystemError()

        try:
            syntaxis = digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError()

    atom_indices_to_be_removed = select(molecular_system, 'molecule_type=="water"', check=False)

    if include_selection is not None:
        atom_indices_included = select(molecular_system, selection=include_selection, syntaxis=syntaxis, check=False)
        atom_indices_to_be_removed = list((set(atom_indices_to_be_removed) | set(atom_indices_included)))

    if exclude_selection is not None:
        atom_indices_excluded = select(molecular_system, selection=exclude_selection, syntaxis=syntaxis, check=False)
        atom_indices_to_be_removed = list((set(atom_indices_to_be_removed) - set(atom_indices_excluded)))

    return remove(molecular_system, atom_indices_to_be_removed)

