from . import molsysviewer as _molsysviewer
from . import nglview as _nglview

_dict_view = {
    'MolSysViewer': _molsysviewer.view,
    'NGLView': _nglview.view,
}
