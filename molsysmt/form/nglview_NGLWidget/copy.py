from copy import copy
from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='nglview.NGLWidget')
def extract(item, skip_digestion=False):

    tmp_item = copy(item)

    return tmp_item

