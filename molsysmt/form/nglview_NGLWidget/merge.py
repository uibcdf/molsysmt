from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='nglview.NGLWidget')
def merge(items, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import merge as merge_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(len(items))]

    if is_all(structure_indices):
        structure_indices = ['all' for ii in range(len(items))]

    items_molsysmt_MolSys = [to_molsysmt_MolSys(item, skip_digestion=True) for item, ii, jj in zip(items, atom_indices, structure_indices)]
    merged_items_molsysmt_MolSys = merge_molsysmt_MolSys(items_molsysmt_MolSys, skip_digestion=True)
    merged_nglview_NGLWidget = molsysmt_MolSys_to_nglview_NGLWidget(merged_items_molsysmt_MolSys, skip_digestion=True)

    return merged_nglview_NGLWidget

