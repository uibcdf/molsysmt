from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.AmberPrmtopFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.AmberPrmtopFile.

    Parameters
    ----------
    item : openmm.AmberPrmtopFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.AmberPrmtopFile
        Copied item.
    """

    raise NotImplementedMethodError()
