from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:amino_acids_3')
def merge(items, group_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form string:amino_acids_3.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    group_indices : str, list, tuple, or numpy.ndarray, default='all'
        Group indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

