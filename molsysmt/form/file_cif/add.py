from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:cif', to_form='file:cif')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form file:cif.

    Parameters
    ----------
    to_item : file:cif
        Target item to modify or add elements to.
    item : file:cif
        Source item in file:cif form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:cif
        Resulting object in file:cif form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

