def to_XYZ(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_xyznpy import to_XYZ as file_xyznpy_to_XYZ

    return file_xyznpy_to_XYZ(item, atom_indices=atom_indices, structure_indices=structure_indices)
