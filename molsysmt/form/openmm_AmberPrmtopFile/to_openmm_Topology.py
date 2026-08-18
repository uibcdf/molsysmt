from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='openmm.AmberPrmtopFile')
@dep_digest('openmm')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.AmberPrmtopFile to openmm.Topology.

    Parameters
    ----------
    item : openmm.AmberPrmtopFile
        Source item in openmm.AmberPrmtopFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.

    .. versionadded:: 1.0.0
    """

    tmp_item = item.topology

    return tmp_item
