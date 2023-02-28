def to_molsysmt_StructuresDict(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_trjpk import to_molsysmt_StructuresDict as file_trjpk_to_molsysmt_StructuresDict

    tmp_item = file_trjpk_to_molsysmt_StructuresDict(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

