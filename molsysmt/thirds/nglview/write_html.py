import nglview as nv

def write_html(view, output_filename):

    from molsysmt.form.nglview_NGLWidget.get import get_n_structures_from_system

    n_structures = get_n_structures_from_system(view)

    nv.write_html(output_filename, [view], frame_range=(0, n_structures))

    pass

