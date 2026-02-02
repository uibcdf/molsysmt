from molsysmt.dependencies import requires

@requires('nglview')
def write_html(view, output_filename):

    import nglview as nv
    from molsysmt.form.nglview_NGLWidget import get_n_structures_from_system

    n_structures = get_n_structures_from_system(view)

    nv.write_html(output_filename, [view], frame_range=(0, n_structures))

    pass

