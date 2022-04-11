from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        digest_item(item_1, 'nglview.NGLWidget')
        digest_item(item_2, 'nglview.NGLWidget')

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import merge as merge_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
    tmp_item_1 = to_molsysmt_MolSys(item_1)
    tmp_item_2 = to_molsysmt_MolSys(item_2)
    tmp_item = merge_molsysmt_MolSys(tmp_item_1, tmp_item_2)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

    return tmp_item

