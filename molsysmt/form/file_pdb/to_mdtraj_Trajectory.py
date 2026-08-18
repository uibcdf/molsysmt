from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:pdb')
@dep_digest('mdtraj')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to mdtraj.Trajectory.

    Parameters
    ----------
    item : file:pdb
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Trajectory
        Converted molecular system representation.
    """

    from mdtraj import load_pdb

    from ..mdtraj_Trajectory.extract import extract as extract_mdtraj_Trajectory

    tmp_item = load_pdb(item)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item
