from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='mdtraj.DCDTrajectoryFile')
@dep_digest('mdtraj')
def to_mdtraj_DCDTrajectoryFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from mdtraj.DCDTrajectoryFile to mdtraj.DCDTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.DCDTrajectoryFile
        Source item in mdtraj.DCDTrajectoryFile form.
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
    mdtraj.DCDTrajectoryFile
        Resulting object in mdtraj.DCDTrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.variables import is_all
    import os

    if isinstance(item, (str, os.PathLike)):
        from mdtraj.formats import DCDTrajectoryFile
        tmp_item = DCDTrajectoryFile(str(item))
    else:
        tmp_item = item

    if not (is_all(atom_indices) and is_all(structure_indices)):
        from .extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

    return tmp_item

