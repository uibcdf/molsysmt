from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.AmberInpcrdFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.AmberInpcrdFile to molsysmt.Structures.

    Parameters
    ----------
    item : openmm.AmberInpcrdFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Structures
        Converted molecular system representation.
    """

    from molsysmt.native import Structures
    from .get_structural_attributes import (get_coordinates_from_atom, get_velocities_from_atom,
                                            get_box_from_system)

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    velocities = get_velocities_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                          skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)

    tmp_item = Structures()
    tmp_item.append(coordinates=coordinates, velocities=velocities, box=box, skip_digestion=True)

    return tmp_item
