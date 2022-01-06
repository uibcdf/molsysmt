def to_molsysmt_MolSys(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.rdkit_Mol import is_rdkit_Mol
    from molsysmt.basic import convert

    if not is_rdkit_Mol(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.MolSys', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

