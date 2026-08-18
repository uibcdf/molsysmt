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
        Source item in openmm.State form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.State
        Resulting object in openmm.State form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

