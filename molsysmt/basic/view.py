from molsysmt._private.digestion import digest
from molsysmt.thirds.nglview import load_html_in_jupyter_notebook
from inspect import stack
from pathlib import Path
from molsysmt.config import _view_from_htmlfiles

@digest()
def view(molecular_system=None, selection='all', structure_indices='all',
         standard=False, with_water_as=None, viewer='NGLView', syntax='MolSysMT'):
    """
    Showing a molecular system.

    This function assists the user in the usage of molecular visualization libraries ("viewer") to show
    molecular systems in a Jupyter notebook.

    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be shown in the Jupyter notebook by the viewer.

    selection : index, tuple, list, numpy.ndarray or str, default 'all'
        Selection of atoms of the molecular system to be shown by the viewer.
        The selection can be given by a list, tuple or numpy array of
        atom indices (0-based integers); or by means of a query string following any of
        :ref:`the selection syntaxes parsable by MolSysMT <Introduction_Selection>`.

    structure_indices : integer, tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) to be shown by the viewer.

    standard : bool, default False
        Option to standardize views with the following features:
            - sdf

    with_water_as :{'licorice', 'surface', None}, default None
        Input argument to choose the water molecules representation.

    viewer : {'NGLView'}, default 'NGLView'
        Molecular visualization library to be used as viewer.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
        it is a string).


    Returns
    -------
    view native object of viewer
        The function returns the visualization native object of the viewer.

    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.

    ArgumentError
        The function raises an ArgumentError in case an input argument value
        does not meet the required conditions.

    SyntaxError
        The function raises a SyntaxError in case the syntax argument takes a not supported value.


    .. versionadded:: 0.1.0


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.

    The list of supported viewers can be checked in the documentation section
    :ref:`User Guide > Introduction > Viewers <Introduction_Viewers>`.


    See Also
    --------

    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> molecular_system = msm.systems.demo['T4 lysozyme L99A']['181l.mmtf']
    >>> msm.basic.view(molecular_system, selection='molecule_type="protein"', viewer='NGLView')
    nglview.NGLWidget()


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > View <Tutorial_View>`.


    """


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


