def from_xtc(item, atom_indices='all', frame_indices='all'):

    from .trajectory import Trajectory
    tmp_item = Trajectory(filepath=item)
    tmp_item.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

