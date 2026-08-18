from .get_structural_attributes import *
from .get_topological_attributes import *

from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.PDBFile')
@dep_digest('mdtraj')
def to_mdtraj_Trajectory(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.PDBFile to mdtraj.Trajectory.

    Parameters
    ----------
    item : openmm.PDBFile
        Source item in openmm.PDBFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.mdtraj_Topology.to_mdtraj_Topology import to_mdtraj_Topology

    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory

    topology = to_mdtraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    tmp_item = mdtraj_Trajectory(positions, topology, skip_digestion=True)

    return tmp_item

