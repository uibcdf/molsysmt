from molsysmt._private.argdigest import arg_digest


@arg_digest()
def show_gui(view):
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

    view.gui_style = 'ngl'

    pass
