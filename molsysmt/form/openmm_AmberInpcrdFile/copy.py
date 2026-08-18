from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.AmberInpcrdFile')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.AmberInpcrdFile.

    Parameters
    ----------
    item : openmm.AmberInpcrdFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.AmberInpcrdFile
        Copied item.
    """

    raise NotImplementedMethodError()

