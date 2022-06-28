from ..exceptions import *

viewers_forms = {
    'NGLView': 'nglview.NGLWidget',
}

viewer_from_lowercase = {ii.lower(): ii for ii in viewers_forms}


def digest_viewer(viewer):
    """ Check if the given viewer is supported by MolSysMT.

        Parameters
        ----------
        viewer : str
            The name of the viewer in lowercase.

        Returns
        -------
        tuple[str, str]
            A tuple with the viewer name and the viewer form.
    """
    try:
        tmp_viewer = viewer_from_lowercase[viewer.lower()]
        tmp_viewer_form = viewers_forms[tmp_viewer]
        return tmp_viewer, tmp_viewer_form
    except KeyError:
        raise BadCallError()
