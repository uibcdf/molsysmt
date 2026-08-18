from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Topology')
def to_mdtraj_Trajectory(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):
    """
    Converting from mdtraj.Topology to mdtraj.Trajectory.

    Parameters
    ----------
    item : mdtraj.Topology
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Trajectory
        Converted molecular system representation.
    """

    from mdtraj.core.trajectory import Trajectory
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = Trajectory(coordinates, item)

    return tmp_item

