from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.AmberRestartFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.AmberRestartFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.AmberRestartFile
        Resulting object in mdtraj.AmberRestartFile form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
