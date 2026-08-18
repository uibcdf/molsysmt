from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.Universe')
def copy(item):
    """
    Creating a copy of an item of form MDAnalysis.Universe.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    MDAnalysis.Universe
        Resulting object in MDAnalysis.Universe form.


    .. versionadded:: 1.0.0
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

