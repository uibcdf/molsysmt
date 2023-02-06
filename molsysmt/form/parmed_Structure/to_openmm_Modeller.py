from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom, get_box_from_system
    from ..openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    coordinates = get_coordinates_from_atom(item, atom_indices=atom_indices,
            structure_indices=structure_indices)
    box = get_box_from_system(item, structure_indices=structure_indices)
    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, coordinates=coordinates, box=box)

    return tmp_item

