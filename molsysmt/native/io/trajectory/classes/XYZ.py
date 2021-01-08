
def from_XYZ(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.trajectory import Trajectory
    from molsysmt.forms.classes.api_XYZ import get_coordinates_from_atom
    tmp_item = Trajectory()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item.append_frames(coordinates=coordinates)
    return tmp_item

def to_XYZ(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Trajectory import get_coordinates_from_atom
    tmp_item = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    return tmp_item
