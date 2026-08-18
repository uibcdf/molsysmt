from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mmcif.PdbxContainers.DataContainer.

    Parameters
    ----------
    item : mmcif.PdbxContainers.DataContainer
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mmcif.PdbxContainers.DataContainer
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

