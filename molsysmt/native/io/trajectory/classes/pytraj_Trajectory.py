
def from_pytraj_Trajectory(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.trajectory import Trajectory
    from molsysmt.forms.classes.api_pytraj_Trajectory import get_frame_from_atom
    tmp_item = Trajectory()
    step, time, coordinates, box = get_frame_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item.set_frames(atom_indices=atom_indices, step=step, time=time, coordinates=coordinates, box=box)
    return tmp_item

