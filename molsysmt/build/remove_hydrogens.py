# ==================================================
# Methods to remove elements from a molecular system
# ==================================================

"""
Remove Atoms
==============
Methods to remove atoms from a molecular model.
"""

def remove_hydrogens (molecular_system, selection="all", include_selection=None, exclude_selection=None, syntaxis="MolSysMT"):

    from molsysmt._private_tools._digestion import digest_syntaxis, digest_molecular_system
    from molsysmt.multitool import select, remove

    molecular_system = digest_molecular_system(molecular_system)
    syntaxis = digest_syntaxis(syntaxis)

    atom_indices_to_be_removed = select(molecular_system, 'atom_type=="H"')

    if include_selection is not None:
        atom_indices_included = select(molecular_system, selection=include_selection, syntaxis=syntaxis)
        atom_indices_to_be_removed = list((set(atom_indices_to_be_removed) | set(atom_indices_included)))

    if exclude_selection is not None:
        atom_indices_excluded = select(molecular_system, selection=exclude_selection, syntaxis=syntaxis)
        atom_indices_to_be_removed = list((set(atom_indices_to_be_removed) - set(atom_indices_excluded)))

    return remove(molecular_system, atom_indices_to_be_removed)

