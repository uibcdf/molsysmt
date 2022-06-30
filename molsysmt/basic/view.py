from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def view(molecular_system=None, viewer='NGLView', selection='all', structure_indices='all',
         concatenate_structures=False, standardize=False, water_as_surface=False, syntaxis='MolSysMT'):

    concatenate=False
    if concatenate_structures:
        concatenate=True

    from . import convert, merge, concatenate_structures, is_molecular_system, are_multiple_molecular_systems
    from molsysmt.thirds.nglview import standardize_view
    from molsysmt.thirds.nglview import show_system_as_transparent_surface

    viewer, form_viewer = digest_viewer(viewer)

    if is_molecular_system(molecular_system):
        tmp_item = convert(molecular_system, to_form=form_viewer, selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)
    elif are_multiple_molecular_systems(molecular_system):
        if concatenate:
            molecular_system = concatenate_structures(molecular_system, selections=selection,
                                                      structure_indices=structure_indices)
        else:
            molecular_system = merge(molecular_system, selections=selection, structure_indices=structure_indices, syntaxis=syntaxis)
        tmp_item = convert(molecular_system, to_form=form_viewer)

    if standardize:
        if viewer=='NGLView':
            standardize_view(tmp_item)

    if water_as_surface:
        if viewer=='NGLView':
            show_system_as_transparent_surface(tmp_item)

    return tmp_item

