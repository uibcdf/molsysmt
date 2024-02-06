from copy import copy
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='nglview.NGLWidget')
def extract(item, skip_digestion=False):

    tmp_item = copy(item)

    return tmp_item

