from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='openmm.Modeller')
@dep_digest('openmm')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form openmm.Modeller.

    Parameters
    ----------
    item : openmm.Modeller
        Source item in openmm.Modeller form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.

    .. versionadded:: 1.0.0
    """

    from openmm.app import Modeller

    if is_all(atom_indices) and is_all(structure_indices):

        tmp_item = Modeller(item.topology, item.positions)

    else:

        from . import get_coordinates_from_atom
        from ..openmm_Topology.extract import extract as extract_openmm_Topology

        tmp_topology = extract_openmm_Topology(item.topology, atom_indices=atom_indices, skip_digestion=True)
        tmp_positions = get_coordinates_from_atom(item, indices=atom_indices, skip_digestion=True)
        tmp_item = Modeller(tmp_topology, tmp_positions)

    return tmp_item

