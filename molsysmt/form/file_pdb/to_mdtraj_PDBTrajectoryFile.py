from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_mdtraj_PDBTrajectoryFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to mdtraj.PDBTrajectoryFile.

    Parameters
    ----------
    item : file:pdb
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.PDBTrajectoryFile
        Converted molecular system representation.
    """

    from mdtraj.formats.pdb import PDBTrajectoryFile
    from ..mdtraj_PDBTrajectoryFile.extract import extract as extract_mdtraj_PDBTrajectoryFile

    tmp_item = PDBTrajectoryFile(item)
    tmp_item = extract_mdtraj_PDBTrajectoryFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

