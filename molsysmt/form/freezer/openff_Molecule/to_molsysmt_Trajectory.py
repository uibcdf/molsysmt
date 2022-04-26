def to_molsysmt_Structures(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.openff_Molecule import is_openff_Molecule
    from molsysmt.basic import convert

    if not is_openff_Molecule(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.Trajectory', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

