from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.Topology')
def merge(items, atom_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form MDAnalysis.Topology.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.Topology
        Resulting object in MDAnalysis.Topology form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

