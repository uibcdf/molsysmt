from .get_structural_attributes import *
from .get_topological_attributes import *

from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.State')
def to_XYZ(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.State to XYZ.

    Parameters
    ----------
    item : openmm.State
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    XYZ
        Converted molecular system representation.
    """


    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)

    return coordinates

