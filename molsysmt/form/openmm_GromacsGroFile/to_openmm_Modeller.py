from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_openmm_Modeller(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'openmm.GromacsGroFile')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller
    from . import get_coordinates_from_atom, get_box_from_atom

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)
    box = get_box_from_atom(item, structure_indices=structure_indices, check=False)

    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, coordinates=coordinates, box=box, check=False)

    return tmp_item

