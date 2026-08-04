from inspect import stack
from pathlib import Path
import os


def view(molecular_system=None, selection='all', structure_indices='all', syntax='MolSysMT',
         skip_digestion=False):

    if os.environ.get("MSM_VIEWS_FROM_HTML_FILES", "").lower() == "true":
        htmlfile = None
        f_locals = None
        for frame_info in stack():
            f_locals = frame_info.frame.f_locals
            if 'molsysviewer_htmlfile' in f_locals or 'nglview_htmlfile' in f_locals:
                htmlfile = f_locals.pop('molsysviewer_htmlfile', None) or f_locals.pop('nglview_htmlfile', None)
                break

        if htmlfile is not None and Path(htmlfile).is_file():
            import molsysviewer as msv
            nb_path = os.environ.get("MSM_DOCS_NOTEBOOK") or f_locals.get('__file__', 'index.ipynb')
            return msv.tools.embed_iframe(htmlfile, path=str(nb_path))
        else:
            raise RuntimeError(
                f"msm.view() was called with MSM_VIEWS_FROM_HTML_FILES=True, but no valid "
                f"molsysviewer_htmlfile target was found in scope (resolved htmlfile={htmlfile})."
            )

    from molsysviewer import new_view

    return new_view(
        molecular_system=molecular_system,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        skip_digestion=skip_digestion,
    )
