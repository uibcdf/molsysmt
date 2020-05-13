def from_h5(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native import Trajectory
    tmp_item = Trajectory(filepath=item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

