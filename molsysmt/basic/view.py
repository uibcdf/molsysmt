from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "view"])
@arg_digest()
def view(
    molecular_system=None,
    selection="all",
    structure_indices="all",
    viewer="MolSysViewer",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Visualizing a molecular system.

    Create a viewer widget, optionally loading a molecular system. None creates
    an empty workspace with MolSysViewer or NGLView, without a molecular payload.


    Parameters
    ----------
    molecular_system : molecular system, default=None
        Molecular system in any supported MolSysMT format, or None to create an
        empty workspace. The source is unchanged by creating the view.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection expression or integer atom indices.
        Without a system, only 'all', None or a flat empty sequence is valid.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
        Without a system, only 'all', None or a flat empty sequence is valid.
    viewer : str, default='MolSysViewer'
        'MolSysViewer' or 'NGLView', matched case-insensitively. An explicit None
        reads configure.default_viewer; omitting the argument uses MolSysViewer.
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
    ArgumentError
        If the source or controls are invalid, including a malformed selection,
        an out-of-range index, or an expression/nonempty axis without a system.
    LibraryNotFoundError
        If the selected viewer dependency is unavailable. Other backends are not
        imported or selected as an automatic fallback.


    Notes
    -----
    - Supported molecular-system forms are described in :ref:`Introduction_Forms`.
    - Selection syntaxes and valid query expressions are described in :ref:`Introduction_Selection`.
    - Selections and structure indices are validated before the viewer backend is created.
    - None does not construct a zero-atom MolSys. Empty selector sequences on
      this absent source keep the workspace empty. With an existing source,
      selectors follow ordinary extraction and backend loading requirements;
      an empty result is not silently replaced by an absent source.
    - The returned object owns its widget resources. Close it when finished.
      Returning a Python widget does not certify browser/WebGL rendering.
    - Documentation's static-HTML mode retains its existing asset requirement;
      it embeds a prepared view rather than constructing a runtime workspace.


    See Also
    --------
    :func:`molsysmt.basic.select`
       Selecting atoms or elements from a molecular system.


    Examples
    --------
    >>> import molsysmt as msm
    >>> workspace = msm.view()
    >>> workspace.molsys is None
    True
    >>> workspace.close()
    >>> molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    >>> widget = msm.view(molsys)
    >>> msm.get_form(widget)
    'molsysviewer.MolSysView'
    >>> widget.close()


    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_View`

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.smonitor import LibraryNotFoundError
    from molsysmt.basic.viewer import _dict_view

    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion, caller="molsysmt.basic.view")

    if viewer not in _dict_view:
        raise LibraryNotFoundError(library=viewer, caller="molsysmt.basic.view")

    if molecular_system is None:
        from ._index_validation import (
            validate_element_indices,
            validate_structure_indices,
        )

        # No source means zero available atoms/structures, not unbounded axes.
        def empty_count(element):
            return 0

        selection = validate_element_indices(
            None,
            selection,
            "atom",
            "selection",
            "molsysmt.view",
            count_getter=empty_count,
        )
        structure_indices = validate_structure_indices(
            None,
            structure_indices,
            "molsysmt.view",
            count_getter=empty_count,
        )
    else:
        from . import select
        from ._index_validation import validate_structure_indices

        selection = select(
            molecular_system,
            selection=selection,
            syntax=syntax,
            skip_digestion=True,
        )
        structure_indices = validate_structure_indices(
            molecular_system, structure_indices, "molsysmt.view"
        )

    return _dict_view[viewer](
        molecular_system=molecular_system,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        skip_digestion=True,
    )
