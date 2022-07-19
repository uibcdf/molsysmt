def to_molsysmt_Structures(item, selection='all', structure_indices='all', syntax='MolSysMT'):

    from molsysmt.tools.file_mmtf import is_file_mmtf
    from molsysmt.basic import convert

    if not is_file_mmtf(item):
        raise ValueError

    tmp_item = convert(item, 'molsysmt.Trajectory', selection=selection, structure_indices=structure_indices,
                       syntax=syntax)

    return tmp_item

