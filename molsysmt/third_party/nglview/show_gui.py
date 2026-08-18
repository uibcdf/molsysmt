def show_gui(view, gui=True):
    """
    Toggling or showing the interactive graphical user interface controls in NGLWidget.

    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer.
    gui : bool, default=True
        Whether GUI controls should be visible.

    .. versionadded:: 1.0.0
    """
    if gui:
        view.display(gui=True)
