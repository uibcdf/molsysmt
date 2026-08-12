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
    """Converting an MDTraj HDF5 reader without changing its cursor.

    The returned in-memory trajectory contains the canonical atom selection and preserves
    the requested structure order. Optional HDF5 fields that ``mdtraj.Trajectory`` cannot
    represent remain available only through native MolSysMT conversions.
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
