import numpy as _np

def from_pdb(item, atom_indices='all', frame_indices='all'):

    from .trajectory import Trajectory
    tmp_item = Trajectory(file_path=item)
    tmp_item.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

