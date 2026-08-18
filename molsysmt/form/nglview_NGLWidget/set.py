from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='nglview.NGLWidget')
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    """
    Setting box to system on form nglview.NGLWidget.

    Parameters
    ----------
    item : nglview.NGLWidget
        Source item in nglview.NGLWidget form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()

@arg_digest(form='nglview.NGLWidget')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    """
    Setting coordinates to system on form nglview.NGLWidget.

    Parameters
    ----------
    item : nglview.NGLWidget
        Source item in nglview.NGLWidget form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()

