from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    from . import to_mdtraj_Topology
    from . import get_coordinates_from_atom, get_box_from_system
    from ..mdtraj_Topology import to_mdtraj_Trajectory as openmm_Topology_to_openmm_Modeller

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    box = get_box_from_system(item, structure_indices=structure_indices)
    tmp_item = mdtraj_Topology_to_mdtraj_Trajectory(tmp_item, coordinates=coordinates, box=box)

    return tmp_item

