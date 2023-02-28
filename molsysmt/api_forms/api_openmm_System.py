def to_openmm_Context(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    return openmm_System_to_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation

    return openmm_System_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices)
