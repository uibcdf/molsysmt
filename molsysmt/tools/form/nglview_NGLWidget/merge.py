from molsysmt.tools.nglview_NGLWidget.is_nglview_NGLWidget import is_nglview_NGLWidget
from molsysmt._private_tools.exceptions import WrongFormError
from molsysmt._private_tools.exceptions import NotImplementedMethodError

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_nglview_NGLWidget(item_1)
        except:
            raise WrongFormError('nglview.NGLWidget')

        try:
            is_nglview_NGLWidget(item_2)
        except:
            raise WrongFormError('nglview.NGLWidget')

    from molsysmt.tools.nglview_NGLWidget import to_molsysmt_MolSys as nglview_NGLWidget_to_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import merge as merge_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
    tmp_item_1 = nglview_NGLWidget_to_molsysmt_MolSys(item_1)
    tmp_item_2 = nglview_NGLWidget_to_molsysmt_MolSys(item_2)
    tmp_item = merge_molsysmt_MolSys(tmp_item_1, tmp_item_2)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

    return tmp_item

