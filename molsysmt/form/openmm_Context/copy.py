from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openmm.Context')
def copy(item):
    """
    Creating a copy of an item of form openmm.Context.

    Parameters
    ----------
    item : openmm.Context
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Context
        Copied item.
    """

    raise NotImplementedMethodError()

