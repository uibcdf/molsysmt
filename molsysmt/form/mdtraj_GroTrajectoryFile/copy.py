from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest(form="mdtraj.GroTrajectoryFile")
@dep_digest("mdtraj")
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.GroTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Source object or file in the form named by this adapter.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.GroTrajectoryFile
        Resulting object in mdtraj.GroTrajectoryFile form.


    Notes
    -----
    Opens an independent read-only cursor at the beginning of the same backing
    file, with an independent mutable topology. It does not copy disk bytes or
    clone the original iteration position. The caller's stream is not advanced
    or closed, including after provider iteration disables its text tell().
    Write-mode handlers are unsupported; source files must remain available.

    .. versionadded:: 1.0.0
    """

    return _open_reader(item, independent_topology=True)


def _open_reader(item, independent_topology=False):
    """Open a read-only cursor without touching the caller's iteration state."""
    if item._mode != "r":
        raise NotImplementedMethodError(
            caller="molsysmt.form.mdtraj_GroTrajectoryFile.copy"
        )
    from copy import deepcopy

    from mdtraj.formats import GroTrajectoryFile

    # Reopen the complete backing input at its beginning. The original text
    # cursor is opaque after the provider's iterator-based read(), so do not
    # call tell()/seek() on the caller's stream.
    return GroTrajectoryFile(
        item._file.name,
        "r",
        top=deepcopy(item.topology) if independent_topology else item.topology,
    )
