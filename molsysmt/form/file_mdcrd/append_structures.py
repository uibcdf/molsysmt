from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mdcrd')
def append_structures(to_item, item, structure_indices='all', skip_digestion=False):
    """
    Appending coordinate structures to an item of form file:mdcrd.

    Parameters
    ----------
    to_item : file:mdcrd
        Target item to modify or add elements to.
    item : file:mdcrd
        Source item in file:mdcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:mdcrd
        Resulting object in file:mdcrd form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
