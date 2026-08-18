from molsysmt._private.argdigest import *
from depdigest import dep_digest

@arg_digest(form='molsysmt.MolSys')
@dep_digest('openmm')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to openmm.Modeller.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.

    .. versionadded:: 1.0.0
    """

    from openmm.app import Modeller

    from .to_openmm_Topology import to_openmm_Topology
    from . import get_coordinates_from_atom
    from molsysmt import pyunitwizard as puw

    tmp_topology = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_positions = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_positions = puw.convert(tmp_positions, to_form='openmm.unit')

    tmp_item = Modeller(tmp_topology, tmp_positions[0])

    return tmp_item

