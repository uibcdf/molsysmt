from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="mdtraj.HDF5TrajectoryFile")
@dep_digest("mdtraj")
def to_mdtraj_Trajectory(
    item,
    atom_indices="all",
    structure_indices="all",
    skip_digestion=False,
):
    """
    Converting from mdtraj.HDF5TrajectoryFile to mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.


    .. versionadded:: 1.0.0
    """

    mdtraj_atom_indices = None
    if not is_all(atom_indices):
        mdtraj_atom_indices = sorted(atom_indices)

    position = item.tell()
    try:
        item.seek(0)
        trajectory = item.read_as_traj(atom_indices=mdtraj_atom_indices)
    finally:
        item.seek(position)

    if not is_all(structure_indices):
        trajectory = trajectory.slice(structure_indices)

    return trajectory
