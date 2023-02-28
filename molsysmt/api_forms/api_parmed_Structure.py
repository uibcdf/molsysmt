## Methods
def to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.parmed_Structure import \
        to_parmed_GromacsTopologyFile as parmed_Structure_to_parmed_GromacsTopologyFile

    return parmed_Structure_to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.parmed_Structure import to_openmm_Topology as parmed_Structure_to_openmm_Topology

    return parmed_Structure_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.parmed_Structure import to_openmm_Modeller as parmed_Structure_to_openmm_Modeller

    return parmed_Structure_to_openmm_Modeller(item, atom_indices=atom_indices,
                                               structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.parmed_Structure import to_mdtraj_Topology as parmed_Structure_to_mdtraj_Topology

    return parmed_Structure_to_mdtraj_Topology(item, atom_indices=atom_indices)


def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.parmed_Structure import to_mdtraj_Trajectory as parmed_Structure_to_mdtraj_Trajectory

    return parmed_Structure_to_mdtraj_Trajectory(item, atom_indices=atom_indices)


def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.parmed_Structure import to_nglview_NGLWidget as parmed_Structure_to_nglview_NGLWidget

    return parmed_Structure_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices)


def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.parmed_Structure import to_file_pdb as parmed_Structure_to_file_pdb

    return parmed_Structure_to_file_pdb(item, atom_indices=atom_indices,
                                        structure_indices=structure_indices, output_filename=output_filename)


def to_file_mol2(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.parmed_Structure import to_file_mol2 as parmed_Structure_to_file_mol2

    return parmed_Structure_to_file_mol2(item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, output_filename=output_filename)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.parmed_Structure import to_molsysmt_MolSys as parmed_Structure_to_molsysmt_MolSys

    return parmed_Structure_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                               structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.parmed_Structure import to_molsysmt_Topology as parmed_Structure_to_molsysmt_Topology

    return parmed_Structure_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.parmed_Structure import to_molsysmt_Structures as parmed_Structure_to_molsysmt_Structures

    return parmed_Structure_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                   structure_indices=structure_indices)
