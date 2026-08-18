from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:top')
def append_structures(to_item, item, structure_indices='all', skip_digestion=False):
    """
    Appending coordinate structures to an item of form file:top.

    Parameters
    ----------
    to_item : file:top
        Target item to modify or add elements to.
    item : file:top
        Source item in file:top form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:top
        Resulting object in file:top form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
