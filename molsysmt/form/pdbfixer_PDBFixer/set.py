from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
def set_group_name_to_group(item, indices='all', value=None, skip_digestion=False):

    """
    Setting group name to group on form pdbfixer.PDBFixer.

    Parameters
    ----------
    item : pdbfixer.PDBFixer
        Source item in pdbfixer.PDBFixer form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
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

