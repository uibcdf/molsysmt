from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md


@digest(form='nglview.NGLWidget')
def clear(view, skip_digestion=False):

    view.clear_representations()

    pass

