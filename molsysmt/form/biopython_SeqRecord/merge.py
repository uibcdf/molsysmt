from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.SeqRecord')
def merge(items, group_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form biopython.SeqRecord.


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
    biopython.SeqRecord
        Resulting object in biopython.SeqRecord form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

