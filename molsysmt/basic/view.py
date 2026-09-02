from molsysmt._private.argdigest import arg_digest


from smonitor import signal

@signal(tags=['api', 'view'])
@arg_digest()
def view(molecular_system=None, selection='all', structure_indices='all',
         viewer='MolSysViewer', syntax='MolSysMT', skip_digestion=False):
    """
    Visualizing a molecular system.

    This function displays a molecular system using an external interactive 3D visualization library
    inside a Jupyter notebook. The visualization backend can be selected by the `viewer` argument.


    Parameters
    ----------
    molecular_system : molecular system, default=None
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    viewer : str, default='MolSysViewer'
        Viewer backend used to create the interactive representation.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Visualization widget returned by the selected viewer. For `'MolSysViewer'`, this is a
        `molsysviewer.MolSysView` instance. For `'NGLView'`, this is an `nglview.NGLWidget` instance.


    Raises
    ------
    NotSupportedFormError
        If the molecular system is provided in an unsupported form.
    ArgumentError
        If one or more input arguments are invalid, including a malformed
        selection or an out-of-range element or structure index.
    ModuleNotFoundError
        If the requested viewer backend is not available in the current environment.


    Notes
    -----
    - Supported molecular-system forms are described in :ref:`Introduction_Forms`.
    - Selection syntaxes and valid query expressions are described in :ref:`Introduction_Selection`.
    - Selections and structure indices are validated before the viewer backend is created.


    See Also
    --------
    :func:`molsysmt.basic.select`
       Selecting atoms or elements from a molecular system.


    Examples
    --------
    The following example illustrates how to visualize only the protein component of a molecular system:

    >>> import molsysmt as msm
    >>> molecular_system = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.basic.view(molecular_system, selection='molecule_type=="protein"')  # doctest: +ELLIPSIS
    <molsysviewer.viewer.MolSysView object at 0x...>

    Select an alternative backend (requires nglview):

    >>> msm.basic.view(molecular_system, selection='molecule_type=="protein"', viewer='NGLView')
    NGLWidget()


    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_View`

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic.viewer import _dict_view
    from molsysmt._private.smonitor import LibraryNotFoundError

    if viewer not in _dict_view:
        raise LibraryNotFoundError(
            library=viewer,
            caller='molsysmt.basic.view'
        )

    if molecular_system is not None:
        from . import select
        from ._index_validation import validate_structure_indices

        selection = select(
            molecular_system,
            selection=selection,
            syntax=syntax,
            skip_digestion=True,
        )
        structure_indices = validate_structure_indices(
            molecular_system, structure_indices, 'molsysmt.view'
        )

    return _dict_view[viewer](
        molecular_system=molecular_system,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        skip_digestion=True,
    )
