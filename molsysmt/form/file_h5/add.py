from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5', to_form='file:h5')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form file:h5.

    Parameters
    ----------
    to_item : file:h5
        Target item to modify or add elements to.
    item : file:h5
        Source item in file:h5 form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:h5
        Resulting object in file:h5 form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

