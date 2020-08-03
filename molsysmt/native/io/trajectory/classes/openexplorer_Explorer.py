
def from_openexplorer_Explorer(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .openmm_Context import from_openmm_Context as molsysmt_Trajectory_from_openmm_Context
    from molsysmt.forms.classes.api_openexplorer_Explorer import to_openmm_Context as openexplorer_Explorer_to_openmm_Context

    tmp_item = openexplorer_Explorer_to_openmm_Context(item)
    tmp_item = molsysmt_Trajectory_from_openmm_Context(tmp_item)

    return tmp_item

