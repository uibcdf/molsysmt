from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.GromacsGroFile')
def copy(item, skip_digestion=True):
    """
    Creating a copy of an item of form openmm.GromacsGroFile.

    Parameters
    ----------
    item : openmm.GromacsGroFile
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.GromacsGroFile
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

