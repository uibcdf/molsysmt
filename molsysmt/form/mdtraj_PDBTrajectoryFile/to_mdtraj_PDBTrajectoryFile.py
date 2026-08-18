from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile')
@dep_digest('mdtraj')
def to_mdtraj_PDBTrajectoryFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from mdtraj.PDBTrajectoryFile to mdtraj.PDBTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.PDBTrajectoryFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.PDBTrajectoryFile
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
                   copy_if_all=copy_if_all, skip_digestion=True)
