
def from_openmm_Context(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.trajectory import Trajectory
    from molsysmt.api_items.api_openmm_Context import get_frame_from_atom

    tmp_item = Trajectory()
    _, time, coordinates, box = get_frame_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    tmp_item.append_structures(coordinates=coordinates, box=box, time=time)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

