from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='nglview.NGLWidget')
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    raise NotImplementedMethodError()

@arg_digest(form='nglview.NGLWidget')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    raise NotImplementedMethodError()

