from molsysmt._private.digestion import digest
from molsysmt.thirds.nglview import load_html_in_jupyter_notebook
from inspect import stack
from pathlib import Path
from molsysmt.config import _view_from_htmlfiles

@digest()
def view(molecular_system=None, viewer='NGLView', selection='all', structure_indices='all',
         standard=False, with_water_as=None, syntax='MolSysMT'):

    if _view_from_htmlfiles:
        if 'nglview_htmlfile' in stack()[2][0].f_locals:
            htmlfile = stack()[2][0].f_locals['nglview_htmlfile']
            if htmlfile is not None:
                if Path(htmlfile).is_file():
                    return load_html_in_jupyter_notebook(htmlfile)

    from . import convert
    from molsysmt.viewer.viewers import viewers_forms

    form_viewer = viewers_forms[viewer]

    tmp_item = convert(molecular_system, to_form=form_viewer, selection=selection,
                        structure_indices=structure_indices, syntax=syntax)

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


