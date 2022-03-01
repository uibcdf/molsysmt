def to_molsysmt_Topology(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_mmtf import is_file_mmtf
    from molsysmt.basic import convert

    if not is_file_mmtf(item):
        raise ValueError

    tmp_item = convert(item, 'molsysmt.Topology', selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

