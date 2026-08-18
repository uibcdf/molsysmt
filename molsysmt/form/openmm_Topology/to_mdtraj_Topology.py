from molsysmt._private.smonitor import LibraryNotFoundError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.Topology to mdtraj.Topology.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.

    .. versionadded:: 1.0.0
    """

    try:
        from mdtraj.core.topology import Topology as mdtraj_Topology
    except Exception:
        raise LibraryNotFoundError('MDTraj')

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    tmp_item = mdtraj_Topology.from_openmm(tmp_item)

    return tmp_item

