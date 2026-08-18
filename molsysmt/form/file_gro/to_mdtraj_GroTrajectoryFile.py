from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_mdtraj_GroTrajectoryFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:gro to mdtraj.GroTrajectoryFile.

    Parameters
    ----------
    item : file:gro
        Source item in file:gro form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.GroTrajectoryFile
        Resulting object in mdtraj.GroTrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    from mdtraj.formats import GroTrajectoryFile
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)
    tmp_item = GroTrajectoryFile(tmp_item)

    return tmp_item

