
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Topology')
def merge(items, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form mdtraj.Topology.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Topology
        Merged item.
    """

    raise NotImplementedMethodError()

