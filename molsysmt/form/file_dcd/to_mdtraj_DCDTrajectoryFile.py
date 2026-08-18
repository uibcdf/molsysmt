from molsysmt._private.argdigest import arg_digest
from molsysmt._private.files_and_directories import str_filename
from depdigest import dep_digest

@arg_digest(form='file:dcd')
@dep_digest('mdtraj')
def to_mdtraj_DCDTrajectoryFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:dcd to mdtraj.DCDTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.DCDTrajectoryFile
        Resulting object in mdtraj.DCDTrajectoryFile form.


    .. versionadded:: 1.0.0
    """

    from mdtraj.formats import DCDTrajectoryFile
    from molsysmt._private.backend_output import silence_backend_stdout
    from ..mdtraj_DCDTrajectoryFile.extract import extract as extract_mdtraj_DCDTrajectoryFile

    # MDTraj announces the detected DCD variant on stdout with no way to turn it off.
    with silence_backend_stdout():
        tmp_item = DCDTrajectoryFile(str_filename(item))
    tmp_item = extract_mdtraj_DCDTrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                structure_indices=structure_indices,
                                                copy_if_all=False, skip_digestion=True)

    return tmp_item
