from copy import copy
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='nglview.NGLWidget')
def extract(item, skip_digestion=False):

    """
    Extracting a subset of elements or structures from form nglview.NGLWidget.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    nglview.NGLWidget
        Resulting object in nglview.NGLWidget form.


    .. versionadded:: 1.0.0
    """
    tmp_item = copy(item)

    return tmp_item

