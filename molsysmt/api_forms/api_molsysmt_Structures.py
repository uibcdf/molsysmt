def to_molsysmt_StructuresDict(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_Structures import \
        to_molsysmt_StructuresDict as molsysmt_Structures_to_molsysmt_StructuresDict

    return molsysmt_Structures_to_molsysmt_StructuresDict(item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices)


def to_XYZ(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_Structures import to_XYZ as molsysmt_Structures_to_XYZ

    return molsysmt_Structures_to_XYZ(item, atom_indices=atom_indices, structure_indices=structure_indices)
