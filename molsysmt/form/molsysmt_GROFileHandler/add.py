from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.GROFileHandler', to_form='molsysmt.GROFileHandler')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form molsysmt.GROFileHandler.

    Parameters
    ----------
    to_item : molsysmt.GROFileHandler
        Target item to modify or add elements to.
    item : molsysmt.GROFileHandler
        Source item in molsysmt.GROFileHandler form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.GROFileHandler
        Resulting object in molsysmt.GROFileHandler form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

