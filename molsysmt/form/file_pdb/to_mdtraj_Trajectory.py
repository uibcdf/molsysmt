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
        Source item in file:pdb form.
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

    from mdtraj import load_pdb

    from ..mdtraj_Trajectory.extract import extract as extract_mdtraj_Trajectory

    tmp_item = load_pdb(item)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item
