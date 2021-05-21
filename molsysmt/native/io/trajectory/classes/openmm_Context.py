
def from_openmm_Context(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.trajectory import Trajectory
    from molsysmt.forms.classes.api_openmm_Context import get_frame_from_atom

    tmp_item = Trajectory()
    _, time, coordinates, box = get_frame_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item.append_frames(coordinates=coordinates, box=box, time=time)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

