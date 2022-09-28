from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='nglview.NGLWidget')
def set_box_to_system(item, structure_indices='all', value=None):

    raise NotImplementedMethodError()

@digest(form='nglview.NGLWidget')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedMethodError()

