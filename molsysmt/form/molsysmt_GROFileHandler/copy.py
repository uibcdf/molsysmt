from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.GROFileHandler')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.GROFileHandler.

    Parameters
    ----------
    item : molsysmt.GROFileHandler
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.GROFileHandler
        Copied item.
    """

    raise NotImplementedMethodError
