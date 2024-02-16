from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from ..openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = openmm_Topology_to_string_pdb_text(tmp_item, coordinates=coordinates, skip_digestion=True)

    return tmp_item

