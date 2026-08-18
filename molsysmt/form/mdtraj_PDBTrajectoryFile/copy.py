from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.PDBTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.PDBTrajectoryFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.PDBTrajectoryFile
        Copied item.
    """

    raise NotImplementedMethodError()
