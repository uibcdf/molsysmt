from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.HDF5TrajectoryFile', to_form='mdtraj.HDF5TrajectoryFile')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form mdtraj.HDF5TrajectoryFile.

    Parameters
    ----------
    to_item : mdtraj.HDF5TrajectoryFile
        Target item to modify or add elements to.
    item : mdtraj.HDF5TrajectoryFile
        Source item in mdtraj.HDF5TrajectoryFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.HDF5TrajectoryFile
        Resulting object in mdtraj.HDF5TrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

