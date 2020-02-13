# =======================
# BUH
# =======================

"""
Remove Atoms
==============

Methods to remove atoms from a molecular model.

"""

def remove_solvent (item, water=True, ions=True, cosolutes=True, include_selection=None, exclude_selection=None,
                   syntaxis='MolModMT'):

    from .utils.selection import digest_syntaxis
    from .multitool import select, remove

    syntaxis = digest_syntaxis(syntaxis)

    atom_indices_to_be_removed = []
    atom_indices_water = []
    atom_indices_ions = []
    atom_indices_cosolutes = []
    atom_indices_included = []
    atom_indices_excluded = []

    if water:

        if syntaxis == 'MolModMT':

            atom_indices_water = select(item, 'molecule.type water', syntaxis=syntaxis)

        elif syntaxis == 'MDTraj':

            from .topology import water_residues
            atom_indices_water = select(item, 'resname '+' '.join([str(ii) for ii in water_residues]),
                                        syntaxis=syntaxis)

        else:

            raise NotImplementedError("Not implemented yet")

    if ions:


        if syntaxis == 'MolModMT':

            atom_indices_ions = select(item, 'molecule.type ion', syntaxis=syntaxis)

        elif syntaxis == 'MDTraj':

            from .topology import ion_residues
            atom_indices_ions = select(item, 'resname '+' '.join(['"'+str(ii)+'"' for ii in ion_residues]),
                                       syntaxis=syntaxis)

        else:

            raise NotImplementedError("Not implemented yet")

    if cosolutes:

        if syntaxis == 'MolModMT':

            atom_indices_cosolutes = select(item, 'molecule.type cosolute', syntaxis=syntaxis)

        elif syntaxis == 'MDTraj':

            raise NotImplementedError("Not implemented yet")

        else:

            raise NotImplementedError("Not implemented yet")

    if include_selection is not None:
        atom_indices_included = select(item, include_selection, syntaxis=syntaxis)

    if exclude_selection is not None:
        atom_indices_excluded = select(item, exclude_selection, syntaxis=syntaxis)

    atom_indices_to_be_removed = list((set(atom_indices_water) | set(atom_indices_ions) | set(atom_indices_cosolutes) | \
                                       set(atom_indices_included)) - set(atom_indices_excluded))

    tmp_item = remove(item, atom_indices_to_be_removed)

    return tmp_item


def remove_hydrogens (item, selection="all", syntaxis="MolModMT"):

    from .utils.selection import digest_syntaxis
    from .multitool import select, remove

    syntaxis = digest_syntaxis(syntaxis)

    atom_indices_hydrogens = []

    if syntaxis == 'MolModMT':

        atom_indices_hydrogens = select(item, 'atom.type "H"', syntaxis=syntaxis)

    elif syntaxis == 'MDTraj':

        atom_indices_hydrogens = select(item, selection="type H", syntaxis=syntaxis)

    else:

        raise NotImplementedError("Not implemented yet")


    atom_indices_selected = select(item, selection=selection, syntaxis=syntaxis)
    atom_indices_to_be_removed = list(set(atom_indices_selected).intersection(set(atom_indices_hydrogens)))

    tmp_item = remove(item, atom_indices_to_be_removed)

    return tmp_item

