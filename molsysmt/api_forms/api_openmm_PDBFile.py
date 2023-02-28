def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology

    return openmm_PDBFile_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_molsysmt_Structures as openmm_PDBFile_to_molsysmt_Structures

    return openmm_PDBFile_to_molsysmt_Structures(item, atom_indices=atom_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_molsysmt_MolSys as openmm_PDBFile_to_molsysmt_MolSys

    return openmm_PDBFile_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_mdtraj_Trajectory as openmm_PDBFile_to_mdtraj_Trajectory

    return openmm_PDBFile_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_mdtraj_Topology as openmm_PDBFile_to_mdtraj_Topology

    return openmm_PDBFile_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Topology import to_openmm_Topology as openmm_PDBFile_to_mdtraj_Topology

    return openmm_PDBFile_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_nglview_NGLWidget as openmm_PDBFile_to_nglview_NGLWidget

    return openmm_PDBFile_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices)
