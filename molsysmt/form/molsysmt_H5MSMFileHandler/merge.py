from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.H5MSMFileHandler')
def merge(items, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.H5MSMFileHandler
        Merged item.
    """

    raise NotImplementedMethodError()

