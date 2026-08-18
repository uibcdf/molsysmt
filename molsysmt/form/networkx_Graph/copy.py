from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='networkx.Graph')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form networkx.Graph.

    Parameters
    ----------
    item : networkx.Graph
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    networkx.Graph
        Copied item.
    """

    tmp_item = item.copy()

    return tmp_item

