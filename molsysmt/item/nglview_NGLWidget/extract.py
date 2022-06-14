from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from copy import copy

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        digest_item(item, 'nglview.NGLWidget')
        indices = digest_indices(indices)
        structure_indices = digest_structure_indices(structure_indices)

    if (atom_indices is 'all') and (structure_indices is 'all'):

        if copy_if_all:
            tmp_item = copy(item)
        else:
            tmp_item = item
    else:

        from . import to_molsysmt_MolSys
        from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
        tmp_item = nglview_NGLWidget_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
        tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

    return tmp_item

