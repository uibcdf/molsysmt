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

    This function displays a molecular system in a Jupyter notebook using an external molecular
    visualization library (viewer). The user can control the level of detail and representation
    for different components of the system, such as water or ions, and apply selections to atoms
    or structures prior to rendering.

    Parameters
    ----------
    molecular_system : molecular system, optional
        Molecular system in any of the :ref:`supported forms <Introduction_Forms>` to be displayed.
        If None, an empty viewer is returned.

    selection : str, tuple, list, or numpy.ndarray, default 'all'
        Selection of atoms to be shown. Can be provided as a list, tuple, or array of atom indices
        (0-based); or as a query string following a :ref:`supported selection syntax <Introduction_Selection>`.

    structure_indices : int, tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) to be displayed in the viewer.

    standard : bool, default True
        Whether to apply a default standardized view layout. This includes basic visual styles and
        coloring schemes appropriate for common systems.

    with_water_as : {'licorice', 'surface', None}, default None
        Optional visual representation to be used for water molecules. If None, water is not displayed.

    with_ions_as : {'licorice', 'balls', 'balls and sticks', None}, default None
        Optional visual representation to be used for ions. If None, ions are not displayed.

    viewer : {'NGLView'}, default 'NGLView'
        Viewer to use for visualization. Currently, only 'NGLView' is supported.

    syntax : str, default 'MolSysMT'
        Selection syntax used to interpret the `selection` string.

    Returns
    -------
    Viewer object
        The visualization widget returned by the selected viewer. For NGLView, this is an
        `nglview.NGLWidget` object.

    Raises
    ------
    NotSupportedFormError
        Raised if the molecular system is provided in an unsupported form.

    ArgumentError
        Raised if input arguments do not meet the required conditions.

    Notes
    -----
    The list of supported molecular system forms is described in:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    For available selection syntaxes, see:
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`

    For a list of supported viewers and their options, see:
    :ref:`User Guide > Introduction > Viewers <Introduction_Viewers>`

    See Also
    --------
    :func:`molsysmt.basic.select`
        Selecting atoms from a molecular system.

    Examples
    --------
    The following example illustrates how to visualize only the protein component of a molecular system:

    >>> import molsysmt as msm
    >>> molecular_system = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.basic.view(molecular_system, selection='molecule_type=="protein"', viewer='NGLView')
    NGLWidget()

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > View <Tutorial_View>`

    .. versionadded:: 0.1.0
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

