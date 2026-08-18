from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openmm.Context')
def copy(item):
    """
    Creating a copy of an item of form openmm.Context.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    openmm.Context
        Resulting object in openmm.Context form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

