from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.System')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.System.

    Parameters
    ----------
    item : openmm.System
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.System
        Copied item.
    """

    tmp_item = item.__copy__()

    return tmp_item

