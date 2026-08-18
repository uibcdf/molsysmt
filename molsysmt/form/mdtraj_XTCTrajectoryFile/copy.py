from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.XTCTrajectoryFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.XTCTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.XTCTrajectoryFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.XTCTrajectoryFile
        Copied item.
    """

    raise NotImplementedMethodError()

