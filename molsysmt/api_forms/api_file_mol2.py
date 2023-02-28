
def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_molsysmt_MolSys as file_mol2_to_molsysmt_MolSys

    return file_mol2_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_molsysmt_Topology as file_mol2_to_molsysmt_Topology

    return file_mol2_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_molsysmt_Structures as file_mol2_to_molsysmt_Structures

    return file_mol2_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_parmed_Structure as file_mol2_to_parmed_Structure

    return file_mol2_to_parmed_Structure(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_mdtraj_Trajectory as file_mol2_to_mdtraj_Trajectory

    return file_mol2_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_mdtraj_Topology as file_mol2_to_mdtraj_Topology

    return file_mol2_to_mdtraj_Topology(item, atom_indices=atom_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_openmm_Topology as file_mol2_to_openmm_Topology

    return file_mol2_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_openmm_Modeller as file_mol2_to_openmm_Modeller

    return file_mol2_to_openmm_Modeller(item, atom_indices=atom_indices,
                                        structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.file_mol2 import to_file_pdb as file_mol2_to_file_pdb

    return file_mol2_to_file_pdb(item, atom_indices=atom_indices,
                                 structure_indices=structure_indices, output_filename=output_filename)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_nglview_NGLWidget as file_mol2_to_nglview_NGLWidget

    return file_mol2_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)
