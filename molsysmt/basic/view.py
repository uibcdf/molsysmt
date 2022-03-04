from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *

def view(molecular_system=None, viewer='NGLView', selection='all', structure_indices='all',
         concatenate_structures=False, standardize=False, water_as_surface=False, syntaxis='MolSysMT'):

    from molsysmt.basic import convert, merge
    from molsysmt.basic import concatenate_structures as __concatenate_structures
    from molsysmt.tools.molecular_systems import is_a_single_molecular_system
    from molsysmt.tools.nglview import standardize_view
    from molsysmt.tools.nglview import show_system_as_transparent_surface

    viewer, form_viewer = digest_viewer(viewer)

    if is_a_single_molecular_system(molecular_system):
        molecular_system = digest_molecular_system(molecular_system)
        tmp_item = convert(molecular_system, to_form=form_viewer, selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)
    else:
        if concatenate_structures:
            molecular_system = __concatenate_structures(molecular_system, selections=selection, structure_indices=structure_indices, syntaxis=syntaxis)
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

