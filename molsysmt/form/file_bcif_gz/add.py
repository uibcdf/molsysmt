from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:bcif.gz', to_form='file:bcif.gz')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form file:bcif.gz.

    Parameters
    ----------
    to_item : file:bcif.gz
        Target item to modify or add elements to.
    item : file:bcif.gz
        Source item in file:bcif.gz form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:bcif.gz
        Resulting object in file:bcif.gz form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

