def from_crd(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_crd import to_mdanalysis_Universe as crd_to_mdanalysis_Universe
    from molsysmt.forms.classes.api_mdanalysis_Universe import to_molsysmt_Trajectory as mdanalysis_Universe_to_molsysmt_Trajectory

    tmp_item = crd_to_mdanalysis_Universe(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = mdanalysis_Universe_to_molsysmt_Trajectory(tmp_item)

    return tmp_item

def to_crd(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError
