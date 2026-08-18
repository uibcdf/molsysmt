from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq')
def merge(items, group_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form biopython.Seq.


    Parameters
    ----------
    items : object
        Argument items.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Argument group_indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

