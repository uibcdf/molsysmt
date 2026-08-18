from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest
import numpy as np

@arg_digest(form='parmed.Structure')
@dep_digest('mdtraj')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from parmed.Structure to mdtraj.Trajectory.

    Parameters
    ----------
    item : parmed.Structure
        Source item in parmed.Structure form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.

    .. versionadded:: 1.0.0
    """

    from .to_mdtraj_Topology import to_mdtraj_Topology
    from mdtraj import Trajectory

    topology = to_mdtraj_Topology(
        item,
        atom_indices=atom_indices,
        skip_digestion=True,
    )
    coordinates = item.get_coordinates('all')
    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices]
    if not is_all(atom_indices):
        coordinates = coordinates[:, atom_indices, :]
    tmp_item = Trajectory(np.asarray(coordinates, dtype=float) / 10.0, topology)

    if item.box is not None:
        box = np.asarray(item.box, dtype=float).reshape((-1, 6))
        if len(box) == 1 and tmp_item.n_frames > 1:
            box = np.repeat(box, tmp_item.n_frames, axis=0)
        elif not is_all(structure_indices):
            box = box[structure_indices]
        tmp_item.unitcell_lengths = box[:, :3] / 10.0
        tmp_item.unitcell_angles = box[:, 3:]

    return tmp_item
