def to_mdtraj_AmberRestartFile(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_inpcrd import is_file_inpcrd
    from molsysmt.basic import convert

    if not is_file_inpcrd(item):
        raise ValueError

    tmp_item = convert(item, 'mdtraj.AmberRestartFile', selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

