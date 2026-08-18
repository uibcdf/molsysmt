from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq')
def merge(items, group_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form biopython.Seq.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.Seq
        Merged item.
    """

    raise NotImplementedMethodError()

