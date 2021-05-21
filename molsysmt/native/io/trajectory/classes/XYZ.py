def from_XYZ(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.trajectory import Trajectory
    from molsysmt.forms.classes.api_XYZ import get_coordinates_from_atom
    tmp_item = Trajectory()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item.append_frames(coordinates=coordinates)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_XYZ(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Trajectory import get_coordinates_from_atom
    tmp_item = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item
