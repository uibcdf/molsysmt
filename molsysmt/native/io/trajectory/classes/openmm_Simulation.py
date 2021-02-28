
def from_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Context import from_openmm_Context as openmm_Context_to_molsysmt_Trajectory
    from molsysmt.forms.classes.api_openmm_Simulation import to_openmm_Context as openmm_Simulation_to_openmm_Context

    tmp_item = openmm_Simulation_to_openmm_Context(item, trajectory_item=trajectory_item,
            atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Context_to_molsysmt_Trajectory(tmp_item)
    return tmp_item

