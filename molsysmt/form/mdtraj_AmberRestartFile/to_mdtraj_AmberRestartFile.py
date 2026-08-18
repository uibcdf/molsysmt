from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='mdtraj.AmberRestartFile')
@dep_digest('mdtraj')
def to_mdtraj_AmberRestartFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from mdtraj.AmberRestartFile to mdtraj.AmberRestartFile.

    Parameters
    ----------
    item : mdtraj.AmberRestartFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.AmberRestartFile
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
                   copy_if_all=copy_if_all, skip_digestion=True)
