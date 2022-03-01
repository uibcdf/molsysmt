def to_molsysmt_Topology(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.rdkit_Mol import is_rdkit_Mol
    from molsysmt.basic import convert

    if not is_rdkit_Mol(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.Topology', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

