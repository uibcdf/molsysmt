from inspect import stack
from pathlib import Path
import os

from depdigest import dep_digest


@dep_digest('nglview')
def view(molecular_system=None, selection='all', structure_indices='all', syntax='MolSysMT',
         skip_digestion=False):

    if os.environ.get("MSM_VIEWS_FROM_HTML_FILES", "").lower() == "true":
        htmlfile = None
        f_locals = None
        for frame_info in stack():
            f_locals = frame_info.frame.f_locals
            if 'nglview_htmlfile' in f_locals or 'molsysviewer_htmlfile' in f_locals:
                htmlfile = f_locals.pop('nglview_htmlfile', None) or f_locals.pop('molsysviewer_htmlfile', None)
                break

        resolved_path = None
        if htmlfile is not None:
            if Path(htmlfile).is_file():
                resolved_path = htmlfile
            else:
                nb_env = os.environ.get("MSM_DOCS_NOTEBOOK")
                if nb_env:
                    nb_p = Path(nb_env).resolve()
                    for p in [nb_p] + list(nb_p.parents):
                        candidate = (p / htmlfile).resolve()
                        if candidate.is_file():
                            resolved_path = htmlfile
                            break
                        candidate2 = (p / "docs" / htmlfile).resolve()
                        if candidate2.is_file():
                            resolved_path = htmlfile
                            break

        if resolved_path is not None:
            from molsysmt.third_party.nglview.load_html_in_jupyter_notebook import load_html_in_jupyter_notebook
            return load_html_in_jupyter_notebook(str(resolved_path))

    if molecular_system is None:
        import nglview as nv
        return nv.NGLWidget()

    from molsysmt import convert

    return convert(
        molecular_system,
        to_form='nglview.NGLWidget',
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        skip_digestion=True,
    )
