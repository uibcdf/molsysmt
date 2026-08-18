from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:mol2 to mdtraj.Trajectory.


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

    from mdtraj import load_mol2
    from ..mdtraj_Trajectory.extract import extract as extract_mdtraj_Trajectory

    tmp_item = load_mol2(item)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, skip_digestion=True)

    return tmp_item

def _to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    return to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                skip_digestion=True)
