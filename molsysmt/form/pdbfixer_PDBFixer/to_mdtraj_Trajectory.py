from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
@dep_digest('mdtraj')
def to_mdtraj_Trajectory(item, atom_indices='all', skip_digestion=False):
    """
    Converting from pdbfixer.PDBFixer to mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.


    .. versionadded:: 1.0.0
    """

    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory

    from molsysmt import pyunitwizard as puw
    from molsysmt.form.mdtraj_Topology.to_mdtraj_Topology import to_mdtraj_Topology
    from . import get_coordinates_from_atom

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(tmp_item, indices=atom_indices, skip_digestion=True)
    coordinates = puw.convert(coordinates, to_unit='nanometer', to_form='openmm.unit')
    tmp_item = mdtraj_Trajectory(coordinates, tmp_item, skip_digestion=True)

    return tmp_item
