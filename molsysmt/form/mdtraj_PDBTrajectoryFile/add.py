from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile', to_form='mdtraj.PDBTrajectoryFile')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form mdtraj.PDBTrajectoryFile.

    Parameters
    ----------
    to_item : mdtraj.PDBTrajectoryFile
        Target item to modify or add elements to.
    item : mdtraj.PDBTrajectoryFile
        Source item in mdtraj.PDBTrajectoryFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.PDBTrajectoryFile
        Resulting object in mdtraj.PDBTrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
