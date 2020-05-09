def from_inpcrd(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native import Trajectory
    tmp_item = Trajectory(file_path=item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

