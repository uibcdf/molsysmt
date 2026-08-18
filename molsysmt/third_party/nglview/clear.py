def clear(view):
    """
    Clearing all visual representations and components from an NGLWidget viewer.

    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer.

    .. versionadded:: 1.0.0
    """
    view.clear_representations()
