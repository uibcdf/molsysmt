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
        Source item in mdtraj.AmberRestartFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.AmberRestartFile
        Resulting object in mdtraj.AmberRestartFile form.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
                   copy_if_all=copy_if_all, skip_digestion=True)
