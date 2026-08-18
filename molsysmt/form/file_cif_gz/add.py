from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:cif.gz', to_form='file:cif.gz')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form file:cif.gz.

    Parameters
    ----------
    to_item : file:cif.gz
        Target item to modify or add elements to.
    item : file:cif.gz
        Source item in file:cif.gz form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:cif.gz
        Resulting object in file:cif.gz form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

