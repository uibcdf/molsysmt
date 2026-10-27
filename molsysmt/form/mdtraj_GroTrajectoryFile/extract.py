from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all


@arg_digest(form="mdtraj.GroTrajectoryFile")
@dep_digest("mdtraj")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting a subset of elements or structures from form mdtraj.GroTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Source object or file in the form named by this adapter.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : bool, default=True
        Whether a complete selection requests an independently owned result.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.GroTrajectoryFile
        Resulting object in mdtraj.GroTrajectoryFile form.


    Notes
    -----
    Only complete-handler extraction is supported. An independent result opens
    at the beginning of the same backing file with copied mutable topology;
    it does not clone the caller's cursor or disk bytes. copy_if_all=False
    returns the source explicitly. Subsets raise NotImplementedMethodError.

    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):
        if copy_if_all:
            from .copy import copy

            tmp_item = copy(item, skip_digestion=True)

        else:
            tmp_item = item
    else:
        raise NotImplementedMethodError()

    return tmp_item
