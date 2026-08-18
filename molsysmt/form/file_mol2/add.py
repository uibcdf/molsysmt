from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2', to_form='file:mol2')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form file:mol2.

    Parameters
    ----------
    to_item : file:mol2
        Target item to modify or add elements to.
    item : file:mol2
        Source item in file:mol2 form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:mol2
        Resulting object in file:mol2 form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

