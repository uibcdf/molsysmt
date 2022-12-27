from molsysmt._private.digestion import digest
from molsysmt.thirds.nglview import load_html_in_jupyter_notebook
from inspect import stack
from pathlib import Path
from molsysmt.config import view_from_htmlfiles

@digest()
def view(molecular_system=None, viewer='NGLView', selection='all', structure_indices='all',
         concatenate_structures=False, standard=False, with_water_as=None, syntax='MolSysMT'):

    if view_from_htmlfiles:
        if 'nglview_htmlfile' in stack()[2][0].f_locals:
            htmlfile = stack()[2][0].f_locals['nglview_htmlfile']
            if htmlfile is not None:
                if Path(htmlfile).is_file():
                    return load_html_in_jupyter_notebook(htmlfile)

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

    if standard:
        if viewer=='NGLView':
            from molsysmt.thirds.nglview import standardize_view
            standardize_view(tmp_item)

    if with_water_as is not None:

        if with_water_as == 'surface':
            if viewer=='NGLView':
                from molsysmt.thirds.nglview import show_system_as_transparent_surface
                show_system_as_transparent_surface(tmp_item)
        elif with_water_as == 'licorice':
            if viewer=='NGLView':
                from molsysmt.thirds.nglview import show_water_as_licorice
                show_water_as_licorice(tmp_item)


    return tmp_item


