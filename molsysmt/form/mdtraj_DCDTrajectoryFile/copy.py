from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.DCDTrajectoryFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.DCDTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.DCDTrajectoryFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.DCDTrajectoryFile
        Copied item.
    """

    raise NotImplementedMethodError()

