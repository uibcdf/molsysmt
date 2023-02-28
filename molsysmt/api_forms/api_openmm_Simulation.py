def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_molsysmt_Topology as openmm_Simulation_to_molsysmt_Topology

    return openmm_Simulation_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_molsysmt_Structures as openmm_Simulation_to_molsysmt_Structures

    return openmm_Simulation_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_molsysmt_MolSys as openmm_Simulation_to_molsysmt_MolSys

    return openmm_Simulation_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_openmm_Topology as openmm_Simulation_to_openmm_Topology

    return openmm_Simulation_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_openmm_Modeller as openmm_Simulation_to_openmm_Modeller

    return openmm_Simulation_to_openmm_Modeller(item, atom_indices=atom_indices,
                                                structure_indices=structure_indices)


def to_openmm_Context(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_openmm_Context as openmm_Simulation_to_openmm_Context

    return openmm_Simulation_to_openmm_Context(item, atom_indices=atom_indices,
                                               structure_indices=structure_indices)


def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_pdbfixer_PDBFixer as openmm_Simulation_to_pdbfixer_PDBFixer

    return openmm_Simulation_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.openmm_Simulation import to_file_pdb as openmm_Simulation_to_file_pdb

    return openmm_Simulation_to_file_pdb(item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, output_filename=output_filename)
