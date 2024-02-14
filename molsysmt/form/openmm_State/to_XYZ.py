from molsysmt._private.digestion import digest

@digest(form='openmm.State')
def to_XYZ(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .get import get_coordinates_from_atom

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)

    return coordinates

