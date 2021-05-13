def from_file_h5(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native import Trajectory
    tmp_item = Trajectory(filepath=item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item, tmp_molecular_system

