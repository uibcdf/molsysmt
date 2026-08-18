from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.XTCTrajectoryFile', to_form='mdtraj.XTCTrajectoryFile')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form mdtraj.XTCTrajectoryFile.

    Parameters
    ----------
    to_item : mdtraj.XTCTrajectoryFile
        Target item to modify or add elements to.
    item : mdtraj.XTCTrajectoryFile
        Source item in mdtraj.XTCTrajectoryFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.XTCTrajectoryFile
        Resulting object in mdtraj.XTCTrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

