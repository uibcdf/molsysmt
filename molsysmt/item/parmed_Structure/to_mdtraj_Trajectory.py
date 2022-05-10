from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'parmed.Structure')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_mdtraj_Topology
    from . import get_coordinates_from_atom, get_box_from_system
    from ..mdtraj_Topology import to_mdtraj_Trajectory as openmm_Topology_to_openmm_Modeller

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)
    box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    tmp_item = mdtraj_Topology_to_mdtraj_Trajectory(tmp_item, coordinates=coordinates, box=box, check=False)

    return tmp_item

