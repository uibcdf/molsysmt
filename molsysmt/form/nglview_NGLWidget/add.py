from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_nglview_NGLWidget import is_nglview_NGLWidget

def add(to_item, item, check=True):

    if check:

        try:
            is_nglview_NGLWidget(item)
        except:
            raise WrongFormError('nglview.NGLWidget')

        try:
            is_nglview_NGLWidget(to_item)
        except:
            raise WrongFormError('nglview.NGLWidget')

    raise NotImplementedMethodError()

