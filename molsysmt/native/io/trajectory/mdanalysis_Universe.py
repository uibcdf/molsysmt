
def from_mdanalysis_Universe(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.trajectory import Trajectory
    from molsysmt.forms.api_mdanalysis_Universe import get_frame_from_atom

    tmp_item = Trajectory()
    step, time, coordinates, box = get_frame_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item.append_frames(step=step, time=time, coordinates=coordinates, box=box)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

