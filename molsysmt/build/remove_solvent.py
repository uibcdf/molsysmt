# ==================================================
# Methods to remove elements from a molecular system
# ==================================================

"""
Remove Atoms
==============
Methods to remove atoms from a molecular model.
"""

def remove_solvent(molecular_system, water=True, ions=True, cosolutes=True, include_selection=None, exclude_selection=None, syntaxis='MolSysMT'):

    from molsysmt._private._digestion import digest_molecular_system, digest_syntaxis
    from molsysmt.basic import select, remove

    molecular_system = digest_molecular_system(molecular_system)
    syntaxis = digest_syntaxis(syntaxis)

    atom_indices_to_be_removed = []
    atom_indices_water = []
    atom_indices_ions = []
    atom_indices_cosolutes = []
    atom_indices_included = []
    atom_indices_excluded = []

    if water:
        atom_indices_water = select(molecular_system, 'group_type=="water"')

    if ions:
        atom_indices_ions = select(molecular_system, 'group_type=="ion"')

    if cosolutes:
        atom_indices_cosolutes = select(molecular_system, 'group_type=="cosolute"')

    atom_indices_to_be_removed = list((set(atom_indices_water) | set(atom_indices_ions) | set(atom_indices_cosolutes)))

    if include_selection is not None:
        atom_indices_included = select(molecular_system, selection=include_selection, syntaxis=syntaxis)
        atom_indices_to_be_removed = list((set(atom_indices_to_be_removed) | set(atom_indices_included)))

    if exclude_selection is not None:
        atom_indices_excluded = select(molecular_system, selection=exclude_selection, syntaxis=syntaxis)
        atom_indices_to_be_removed = list((set(atom_indices_to_be_removed) - set(atom_indices_excluded)))

    return remove(molecular_system, atom_indices_to_be_removed)

