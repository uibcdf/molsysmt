from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from copy import copy

@arg_digest(form='string:amino_acids_3')
def extract(item, group_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form string:amino_acids_3.

    Parameters
    ----------
    item : string:amino_acids_3
        Source item in string:amino_acids_3 form.
    group_indices : str, list, tuple, or numpy.ndarray, default='all'
        Group indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.

    .. versionadded:: 1.0.0
    """

    if is_all(group_indices):

        if copy_if_all:
            tmp_item = copy(item)
        else:
            tmp_item = item
    else:

        raise NotImplementedMethodError

    return tmp_item

