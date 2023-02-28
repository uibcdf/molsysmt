def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Modeller import to_mdtraj_Trajectory as openmm_Modeller_to_mdtraj_Trajectory

    return openmm_Modeller_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Modeller import to_mdtraj_Topology as openmm_Modeller_to_mdtraj_Topology

    return openmm_Modeller_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):
    from molsysmt.form.openmm_Modeller import to_openmm_System as openmm_Modeller_to_openmm_System

    return openmm_Modeller_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                            forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm',
                                            constraints=None,
                                            rigid_water=True, remove_cm_motion=True, hydrogen_mass=None,
                                            switch_distance=None,
                                            flexible_constraints=False)


def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):
    from molsysmt.form.openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    return openmm_Modeller_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                forcefield=None, non_bonded_method='no_cutoff',
                                                non_bonded_cutoff='1.0 nm', constraints=None,
                                                rigid_water=True, remove_cm_motion=True, hydrogen_mass=None,
                                                switch_distance=None,
                                                flexible_constraints=False, integrator='Langevin',
                                                temperature='300.0 K',
                                                collisions_rate='1.0 1/ps', integration_timestep='2.0 fs',
                                                platform='CUDA')


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Modeller import to_openmm_Topology as openmm_Modeller_to_openmm_Topology

    return openmm_Modeller_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Modeller import to_pdbfixer_PDBFixer as openmm_Modeller_to_pdbfixer_PDBFixer

    return openmm_Modeller_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Modeller import to_molsysmt_Topology as openmm_Modeller_to_molsysmt_Topology

    return openmm_Modeller_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Modeller import to_molsysmt_Structures as openmm_Modeller_to_molsysmt_Structures

    return openmm_Modeller_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Modeller import to_molsysmt_MolSys as openmm_Modeller_to_molsysmt_MolSys

    return openmm_Modeller_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.openmm_Modeller import to_file_pdb as openmm_Modeller_to_file_pdb

    return openmm_Modeller_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                       output_filename=output_filename)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Modeller import to_nglview_NGLWidget as openmm_Modeller_to_nglview_NGLWidget

    return openmm_Modeller_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices)
