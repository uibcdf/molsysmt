
def to_file_mmtf(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.mmtf_MMTFDecoder import to_file_mmtf as mmtf_MMTFDecoder_to_file_mmtf

    return mmtf_MMTFDecoder_to_file_mmtf(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                         output_filename=output_filename)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.mmtf_MMTFDecoder import to_file_pdb as mmtf_MMTFDecoder_to_file_pdb

    return mmtf_MMTFDecoder_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                        output_filename=output_filename)

def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_string_pdb_text as mmtf_MMTFDecoder_to_string_pdb_text

    return mmtf_MMTFDecoder_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all', bioassembly_name=None):
    from molsysmt.form.mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys

    return mmtf_MMTFDecoder_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, bioassembly_name=None)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology

    return mmtf_MMTFDecoder_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_molsysmt_Structures as mmtf_MMTFDecoder_to_molsysmt_Structures

    return mmtf_MMTFDecoder_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_mdtraj_Trajectory as mmtf_MMTFDecoder_to_mdtraj_Trajectory

    return mmtf_MMTFDecoder_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_openmm_Topology as mmtf_MMTFDecoder_to_openmm_Topology

    return mmtf_MMTFDecoder_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_string_aminoacids1 as mmtf_MMTFDecoder_to_string_aminoacids1

    from molsysmt.form.mmtf_MMTFDecoder import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return mmtf_MMTFDecoder_to_string_aminoacids1(item, group_indices=group_indices)


def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_string_aminoacids3 as mmtf_MMTFDecoder_to_string_aminoacids3

    from molsysmt.form.mmtf_MMTFDecoder import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)
    return mmtf_MMTFDecoder_to_string_aminoacids3(item, group_indices=group_indices)
