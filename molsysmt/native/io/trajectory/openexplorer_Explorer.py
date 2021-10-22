
def from_openexplorer_Explorer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_openexplorer_Explorer import to_molsyst_Trajectory as openexplorer_Explorer_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = openexplorer_Explorer_to_molsysmt_Trajectory(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

