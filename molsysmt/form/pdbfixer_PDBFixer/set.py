from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBFixer')
def set_group_name_to_group(item, indices='all', value=None, skip_digestion=False):

    for group in tmp_item.topology.groups():
        if group.index in indices:
            name = value[np.where(indices == group.index)[0][0]]
            group.name = name
    for bond in tmp_item.topology.bonds():
        for ii in [0,1]:
            if bond[ii].group.index in set_indices:
                name = kwargs[option][np.where(array_indices == bond[ii].group.index)[0][0]]
                bond[ii].group.name = name

    pass

