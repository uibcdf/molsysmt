from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.Universe')
def copy(item):
    """
    Creating a copy of an item of form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    MDAnalysis.Universe
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

