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
        Source item in openmm.State form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    XYZ
        Resulting object in XYZ form.

    .. versionadded:: 1.0.0
    """


    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)

    return coordinates

