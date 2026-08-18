from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.GroTrajectoryFile', to_form='mdtraj.GroTrajectoryFile')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form mdtraj.GroTrajectoryFile.

    Parameters
    ----------
    to_item : mdtraj.GroTrajectoryFile
        Target item to modify or add elements to.
    item : mdtraj.GroTrajectoryFile
        Source item in mdtraj.GroTrajectoryFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.GroTrajectoryFile
        Resulting object in mdtraj.GroTrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
