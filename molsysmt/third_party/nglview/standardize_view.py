def standardize_view(view):
    """
    Applying standardized camera perspective and background rendering settings to an NGLWidget view.

    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer.

    .. versionadded:: 1.0.0
    """
    view.camera = 'orthographic'
    view.background = 'white'
