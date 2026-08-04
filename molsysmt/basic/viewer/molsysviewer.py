from inspect import stack
from pathlib import Path
import os


def view(molecular_system=None, selection='all', structure_indices='all', syntax='MolSysMT',
         skip_digestion=False):

    if os.environ.get("MSM_VIEWS_FROM_HTML_FILES", "").lower() == "true":
        for frame_info in stack():
            f_locals = frame_info.frame.f_locals
            htmlfile = f_locals.get('molsysviewer_htmlfile') or f_locals.get('nglview_htmlfile')
            if htmlfile is not None and Path(htmlfile).is_file():
                import molsysviewer as msv
                nb_path = f_locals.get('__file__', 'index.ipynb')
                return msv.tools.embed_iframe(htmlfile, path=str(nb_path), skip_digestion=True)

    from molsysviewer import new_view

    return new_view(
        molecular_system=molecular_system,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        skip_digestion=skip_digestion,
    )
