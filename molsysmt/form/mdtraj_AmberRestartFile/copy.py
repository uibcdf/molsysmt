from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.AmberRestartFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.AmberRestartFile.

    Parameters
    ----------
    item : mdtraj.AmberRestartFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.AmberRestartFile
        Copied item.
    """

    raise NotImplementedMethodError()
