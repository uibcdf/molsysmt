from os.path import basename as _basename
from nglview import widget as _nglview_widget

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'nglview': form_name,
    _nglview_widget.NGLWidget: form_name
    }
