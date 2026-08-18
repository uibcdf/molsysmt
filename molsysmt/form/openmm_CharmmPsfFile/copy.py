from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.CharmmPsfFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.CharmmPsfFile.

    Parameters
    ----------
    item : openmm.CharmmPsfFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.CharmmPsfFile
        Copied item.
    """

    raise NotImplementedMethodError()

