from depdigest import dep_digest

@dep_digest('nglview')
def write_html(view, output_filename):
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

    import nglview as nv
    from molsysmt.form.nglview_NGLWidget import get_n_structures_from_system

    n_structures = get_n_structures_from_system(view)

    nv.write_html(output_filename, [view], frame_range=(0, n_structures))

    pass

