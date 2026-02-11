from inspect import stack
from pathlib import Path
import os

from depdigest import dep_digest


@dep_digest('nglview')
def view(molecular_system=None, selection='all', structure_indices='all', syntax='MolSysMT',
         skip_digestion=False):

    if os.environ.get("MSM_VIEWS_FROM_HTML_FILES", "").lower() == "true":
        if 'nglview_htmlfile' in stack()[2][0].f_locals:
            htmlfile = stack()[2][0].f_locals['nglview_htmlfile']
            if htmlfile is not None:
                if Path(htmlfile).is_file():
                    from molsysmt.thirds.nglview import load_html_in_jupyter_notebook
                    return load_html_in_jupyter_notebook(htmlfile)

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
