from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Topology')
def to_mdtraj_Trajectory(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):
    """
    Converting from mdtraj.Topology to mdtraj.Trajectory.

    Parameters
    ----------
    item : mdtraj.Topology
        Source item in mdtraj.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    box : numpy.ndarray or quantity
        Simulation box vectors in nanometers.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.

    .. versionadded:: 1.0.0
    """

    from mdtraj.core.trajectory import Trajectory
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = Trajectory(coordinates, item)

    return tmp_item

