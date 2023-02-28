def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_StructuresDict import to_molsysmt_Structures as StructuresDict_to_molsysmt_Structures

    tmp_item = StructuresDict_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def to_file_trjpk(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.molsysmt_StructuresDict import to_file_trjpk as StructuresDict_to_file_trjpk

    tmp_item = StructuresDict_to_file_trjpk(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename)

    return tmp_item

