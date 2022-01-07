def to_molsysmt_MolSys(item, selection='all', model_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.string_smiles import is_string_smiles
    from molsysmt.basic import convert

    if not is_string_smiles(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.MolSys', selection=selection, frame_indices=model_indices, syntaxis=syntaxis)

    return tmp_item

