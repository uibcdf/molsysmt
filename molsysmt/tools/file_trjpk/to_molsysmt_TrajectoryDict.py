def to_molsysmt_TrajectoryDict(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_trjpk import is_file_trjpk
    from molsysmt.basic import convert

    if not is_file_trjpk(item):
        raise ValueError

    tmp_item = convert(item, 'molsysmt.TrajectoryDict', selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

