from molsysmt._private.digestion import digest
from molsysmt.thirds.nglview import load_html_in_jupyter_notebook
from inspect import stack
from pathlib import Path
import os

@digest()
def view(molecular_system=None, selection='all', structure_indices='all',
         standard=True, with_water_as=None, with_ions_as=None,
         viewer='NGLView', syntax='MolSysMT', skip_digestion=False):
    """
    Visualizing a molecular system.

    This function displays a molecular system using an external interactive 3D visualization library (viewer) inside a
    Jupyter notebook. The visualization can be customized by selecting specific atoms or
    structures, choosing representations for water and ions, and applying a standardized
    visual layout.

    Parameters
    ----------
    molecular_system : molecular system, optional
        Molecular system to be displayed. It can be in any of the :ref:`supported forms <Introduction_Forms>`.
        If `None`, an empty viewer is returned.
    selection : str, tuple, list or numpy.ndarray, default='all'
        Selection of atoms to be shown. It can be a list/array of 0-based indices, or a query string
        using one of the :ref:`supported selection syntaxes <Introduction_Selection>`. The default `'all'`
        includes all atoms in the system.
    structure_indices : int, tuple, list, numpy.ndarray or 'all', default='all'
        0-based indices of structures to be shown. The default `'all'` includes all structures.
    standard : bool, default=True
        Whether to apply a default standardized visual layout. This includes representations and
        color schemes for typical biomolecular systems.
    with_water_as : {'licorice', 'surface', None}, default=None
        Representation used for water molecules. If `None`, water is not displayed.
    with_ions_as : {'licorice', 'balls', 'balls and sticks', None}, default=None
        Representation used for ions. If `None`, ions are not displayed.
    viewer : {'NGLView'}, default='NGLView'
        Viewer backend to use for visualization. Currently, only `'NGLView'` is supported.
    syntax : str, default='MolSysMT'
        Syntax used to interpret the `selection` string. See :ref:`Introduction_Selection` for details.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.

    Returns
    -------
    object
        Visualization widget returned by the selected viewer. For `'NGLView'`, this is an
        `nglview.NGLWidget` instance.

    Raises
    ------
    NotSupportedFormError
        If the molecular system is provided in an unsupported form.
    ArgumentError
        If one or more input arguments are invalid.

    Notes
    -----
    - Supported molecular-system forms are described in :ref:`Introduction_Forms`.
    - Selection syntaxes and valid query expressions are described in :ref:`Introduction_Selection`.
    - Currently, the only supported viewer is `'NGLView'`.
    - The standardized visual layout includes cartoon representations for proteins, licorice for
    ligands, and appropriate color schemes. See :ref:`Tutorial_View` for details.

    See Also
    --------
    :func:`molsysmt.basic.select`
       Selecting atoms or elements from a molecular system.

    Examples
    --------
    The following example illustrates how to visualize only the protein component of a molecular system:

    >>> import molsysmt as msm
    >>> molecular_system = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.basic.view(molecular_system, selection='molecule_type=="protein"', viewer='NGLView')
    NGLWidget()

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_View`

    .. versionadded:: 1.0.0
    """

    if os.environ.get("MSM_VIEWS_FROM_HTML_FILES", "").lower() == "true":
        if 'nglview_htmlfile' in stack()[2][0].f_locals:
            htmlfile = stack()[2][0].f_locals['nglview_htmlfile']
            if htmlfile is not None:
                if Path(htmlfile).is_file():
                    return load_html_in_jupyter_notebook(htmlfile)

    from . import convert
    from molsysmt.supported.viewers import viewers_forms

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
                from molsysmt.thirds.nglview import show_as_surface
                show_as_surface(tmp_item, selection='molecule_type=="water"',
                                opacity=0.2, color='lightblue', skip_digestion=True)
        elif with_water_as == 'licorice':
            if viewer=='NGLView':
                from molsysmt.thirds.nglview import show_as_licorice
                show_as_licorice(tmp_item, selection='molecule_type=="water"')

    if with_ions_as is not None:

        if with_ions_as == 'licorice':
            if viewer=='NGLView':
                from molsysmt.thirds.nglview import show_as_licorice
                show_as_licorice(tmp_item, selection='molecule_type=="ion"')
        elif with_ions_as in ['balls and sticks', 'balls']:
            if viewer=='NGLView':
                from molsysmt.thirds.nglview import show_as_balls_and_sticks
                show_as_balls_and_sticks(tmp_item)


    return tmp_item

