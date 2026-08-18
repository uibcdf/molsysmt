from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.SeqRecord', to_form='biopython.SeqRecord')
def add(to_item, item, group_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form biopython.SeqRecord.

    Parameters
    ----------
    to_item : biopython.SeqRecord
        Target item to modify or add elements to.
    item : biopython.SeqRecord
        Source item in biopython.SeqRecord form.
    group_indices : str, list, tuple, or numpy.ndarray, default='all'
        Group indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.SeqRecord
        Resulting object in biopython.SeqRecord form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

