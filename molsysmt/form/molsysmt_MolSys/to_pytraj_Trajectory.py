from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_pytraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to pytraj.Trajectory.


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
    pytraj.Trajectory
        Resulting object in pytraj.Trajectory form.


    .. versionadded:: 1.0.0
    """

    from .to_pytraj_Topology import to_pytraj_Topology
    from molsysmt.form.pytraj_Topology.to_pytraj_Trajectory import to_pytraj_Trajectory as pytraj_Topology_to_pytraj_Trajectory
    from . import get_coordinates_from_atom, get_box_from_system

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)

    tmp_item = to_pytraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = pytraj_Topology_to_pytraj_Trajectory(tmp_item, coordinates=coordinates, box=box, skip_digestion=True)

    return tmp_item
