from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.System')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.System.

    Parameters
    ----------
    item : openmm.System
        Source item in openmm.System form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.System
        Resulting object in openmm.System form.

    .. versionadded:: 1.0.0
    """

    tmp_item = item.__copy__()

    return tmp_item

