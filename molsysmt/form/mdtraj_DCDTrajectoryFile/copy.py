from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.DCDTrajectoryFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.DCDTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.DCDTrajectoryFile
        Source item in mdtraj.DCDTrajectoryFile form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.DCDTrajectoryFile
        Resulting object in mdtraj.DCDTrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

