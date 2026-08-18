from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.GroTrajectoryFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.GroTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.GroTrajectoryFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.GroTrajectoryFile
        Copied item.
    """

    raise NotImplementedMethodError()
