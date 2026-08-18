from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:amino_acids_3', to_form='string:amino_acids_3')
def add(to_item, item, group_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form string:amino_acids_3.

    Parameters
    ----------
    to_item : string:amino_acids_3
        Target item to modify or add elements to.
    item : string:amino_acids_3
        Source item in string:amino_acids_3 form.
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

