from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.H5MSMFileHandler', to_form='molsysmt.H5MSMFileHandler')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    to_item : molsysmt.H5MSMFileHandler
        Target item to modify or add elements to.
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.H5MSMFileHandler
        Resulting object in molsysmt.H5MSMFileHandler form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

