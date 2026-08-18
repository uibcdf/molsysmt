from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openmm.State')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.State.

    Parameters
    ----------
    item : openmm.State
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.State
        Copied item.
    """

    raise NotImplementedMethodError()

