# =======================
# BUH
# =======================

"""
Remove Atoms
==============

Methods to remove atoms from a molecular model.

"""

def remove_solvent (item, water=True, cosolutes=True, include_selection=None, exclude_selection=None,
                   syntaxis='MolModMT'):

    from .utils.selection import digest_syntaxis
    from .multitool import select, remove
    from .topology import water_residues
    from .topology import ion_residues

    syntaxis = digest_syntaxis(syntaxis)

    atom_indices_to_be_removed = []
    atom_indices_water = []
    atom_indices_ions = []
    atom_indices_included = []
    atom_indices_excluded = []

    if water:

        if syntaxis == 'MDTraj':
            atom_indices_water = select(item, 'resname '+' '.join([str(ii) for ii in water_residues]),
                                        syntaxis='MDTraj')

        elif syntaxis == 'MolModMT':
            atom_indices_water = select(item, 'molecule.type water'))

        else:
            not implemented

    if cosolutes:
        atom_indices_ions = select(item, 'resname '+' '.join(['"'+str(ii)+'"' for ii in ion_residues]),
                                    syntaxis='MDTraj')

    if include_selection is not None:
        atom_indices_included = select(item, include_selection, syntaxis=syntaxis)

    if exclude_selection is not None:
        atom_indices_excluded = select(item, exclude_selection, syntaxis=syntaxis)

    atom_indices_to_be_removed = list((set(atom_indices_water) | set(atom_indices_ions) | \
                                       set(atom_indices_included)) - set(atom_indices_excluded))
    atom_indices_to_be_removed = list(_sort(atom_indices_to_be_removed))

    tmp_item = trim(item, atom_indices_to_be_removed)

    return tmp_item


def remove_hydrogens (item, selection="all", syntaxis="mdtraj"):

    from molmodmt import select
    from molmodmt import trim

    atom_indices_selected = select(item, selection=selection, syntaxis=syntaxis)
    atom_indices_hydrogens = select(item, selection="type H", syntaxis=syntaxis)
    atom_indices_to_be_removed = list(set(atom_indices_selected).intersection(set(atom_indices_hydrogens)))
    atom_indices_to_be_removed = list(_sort(atom_indices_to_be_removed))

    tmp_item = trim(item, atom_indices_to_be_removed)

    return tmp_item

