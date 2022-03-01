def to_openmm_Modeller(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_pdb import is_file_pdb
    from molsysmt.basic import convert

    if not is_file_pdb(item):
        raise ValueError

    tmp_item = convert(item, 'openmm.Modeller', selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

