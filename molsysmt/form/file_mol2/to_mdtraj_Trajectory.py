from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:mol2 to mdtraj.Trajectory.

    Parameters
    ----------
    item : file:mol2
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Trajectory
        Converted molecular system representation.
    """

    from mdtraj import load_mol2
    from ..mdtraj_Trajectory.extract import extract as extract_mdtraj_Trajectory

    tmp_item = load_mol2(item)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, skip_digestion=True)

    return tmp_item

def _to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    return to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                skip_digestion=True)
