def write_html(view, filename):
    """
    Exporting an interactive 3D scene from NGLWidget to a standalone HTML file.

    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer.
    filename : str or pathlib.Path
        Output HTML file path.

    .. versionadded:: 1.0.0
    """
    from nglview import write_html as _write_html
    _write_html(filename, view)
