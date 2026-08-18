from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='networkx.Graph')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form networkx.Graph.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    networkx.Graph
        Resulting object in networkx.Graph form.


    .. versionadded:: 1.0.0
    """

    tmp_item = item.copy()

    return tmp_item

