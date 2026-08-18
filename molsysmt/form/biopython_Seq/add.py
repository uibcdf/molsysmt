from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq', to_form='biopython.Seq')
def add(to_item, item, group_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form biopython.Seq.

    Parameters
    ----------
    to_item : biopython.Seq
        Target item to modify or add elements to.
    item : biopython.Seq
        Source item in biopython.Seq form.
    group_indices : str, list, tuple, or numpy.ndarray, default='all'
        Group indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

