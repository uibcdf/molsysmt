from molsysmt._private.digestion import digest
from molsysmt import __sphinxworking__
from molsysmt.thirds.nglview import load_html_in_jupyter_notebook
from inspect import stack

@digest()
def view(molecular_system=None, viewer='NGLView', selection='all', structure_indices='all',
         concatenate_structures=False, standardize=False, water_as_surface=False, syntax='MolSysMT'):

    concatenate=False
    if concatenate_structures:
        concatenate=True

    from . import convert, merge, concatenate_structures, is_a_molecular_system, are_multiple_molecular_systems
    from molsysmt.viewer.viewers import viewers_forms

    form_viewer = viewers_forms[viewer]

    if is_a_molecular_system(molecular_system):
        tmp_item = convert(molecular_system, to_form=form_viewer, selection=selection,
                           structure_indices=structure_indices, syntax=syntax)
    elif are_multiple_molecular_systems(molecular_system):
        if concatenate:
            molecular_system = concatenate_structures(molecular_system, selections=selection,
                                                      structure_indices=structure_indices)
        else:
            molecular_system = merge(molecular_system, selections=selection, structure_indices=structure_indices,
                                     syntax=syntax)
        tmp_item = convert(molecular_system, to_form=form_viewer)

    if standardize:
        if viewer=='NGLView':
            from molsysmt.thirds.nglview import standardize_view
            standardize_view(tmp_item)

    if water_as_surface:
        if viewer=='NGLView':
            from molsysmt.thirds.nglview import show_system_as_transparent_surface
            show_system_as_transparent_surface(tmp_item)

    if __sphinxworking__:

        htmlfile = stack()[2][0].f_locals['nglview_htmlfiles'].pop(0)

        return load_html_in_jupyter_notebook(htmlfile)
    
    return tmp_item


