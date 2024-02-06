from copy import copy
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='nglview.NGLWidget')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            tmp_item = copy(item)
        else:
            tmp_item = item
    else:

        from . import to_molsysmt_MolSys
        from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
        tmp_item = nglview_NGLWidget_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)
        tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

    return tmp_item

