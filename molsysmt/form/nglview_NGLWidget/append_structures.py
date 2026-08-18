from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='nglview.NGLWidget')
def append_structures(item, structure_id=None, time=None, coordinates=None, velocities=None, box=None, skip_digestion=False):
    """
    Appending coordinate structures to an item of form nglview.NGLWidget.

    Parameters
    ----------
    item : nglview.NGLWidget
        Target item.
    structure_id : object, optional
        Structure identifier.
    time : object, optional
        Time coordinates.
    coordinates : object, optional
        Cartesian coordinate array in nanometers.
    box : object, optional
        Box vectors in nanometers.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    nglview.NGLWidget
        Updated item with appended structures.
    """

    raise NotImplementedMethodError()

