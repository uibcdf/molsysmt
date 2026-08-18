from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_mdtraj_PDBTrajectoryFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to mdtraj.PDBTrajectoryFile.

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
    mdtraj.PDBTrajectoryFile
        Resulting object in mdtraj.PDBTrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    from mdtraj.formats.pdb import PDBTrajectoryFile
    from ..mdtraj_PDBTrajectoryFile.extract import extract as extract_mdtraj_PDBTrajectoryFile

    tmp_item = PDBTrajectoryFile(item)
    tmp_item = extract_mdtraj_PDBTrajectoryFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

