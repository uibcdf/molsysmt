
def from_openmm_Simulation(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from .openmm_Context import from_openmm_Context as openmm_Context_to_molsysmt_Trajectory
    from molsysmt.api_forms.api_openmm_Simulation import to_openmm_Context as openmm_Simulation_to_openmm_Context

    tmp_item, tmp_molecular_system = openmm_Simulation_to_openmm_Context(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_Context_to_molsysmt_Trajectory(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices)

    return tmp_item, tmp_molecular_system

