from molsysmt._private_tools.exceptions import BadCallError

viewers_forms = {
    'NGLView' : 'nglview.NGLWidget',
}

viewer_from_lowercase={ ii.lower() : ii for ii in viewers_forms }

def digest_viewer(viewer):

    try:
        tmp_viewer = viewer_from_lowercase[viewer.lower()]
        tmp_viewer_form = viewers_forms[tmp_viewer]
        return tmp_viewer, tmp_viewer_form
    except:
        raise BadCallError()

