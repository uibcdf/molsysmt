from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='nglview.NGLWidget', to_form='nglview.NGLWidget')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

