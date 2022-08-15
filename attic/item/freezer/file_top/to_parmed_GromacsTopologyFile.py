def to_parmed_GromacsTopologyFile(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_top import is_file_top
    from molsysmt.basic import convert

    if not is_file_top(item):
        raise ValueError

    tmp_item = convert(item, 'parmed.GromacsTopologyFile', selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

