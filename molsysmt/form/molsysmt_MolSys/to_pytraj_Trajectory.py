from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_pytraj_Trajectory(item, atom_indices='all', structure_indices='all', digest=True):

    from . import to_pytraj_Topology
    from ..pytraj_Topology import to_pytraj_Trajectory as pytraj_Topology_to_pytraj_Trajectory
    from . import get_coordinates_from_atom, get_box_from_system

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, digest=False)
    box = get_box_from_system(item, structure_indices=structure_indices, digest=False)

    tmp_item = to_pytraj_Topology(item, atom_indices=atom_indices, digest=False)
    tmp_item = pytraj_Topology_to_pytraj_Trajectory(tmp_item, coordinates=coordinates, box=box, digest=False)

    return tmp_item

