def to_molsysmt_Structures(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.XYZ import to_molsysmt_Structures as XYZ_to_molsysmt_Structures

    return XYZ_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_file_xyznpy(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.XYZ import to_file_xyznpy as XYZ_to_file_xyznpy

    return XYZ_to_file_xyznpy(item, atom_indices=atom_indices, structure_indices=structure_indices)
