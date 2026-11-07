from pathlib import Path

from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest()
@dep_digest("nglview")
def write_html(view, output_filename, skip_digestion=False):
    """Exporting one molecular viewer and its dependencies to standalone HTML.

    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer. Independent widgets in the same Python process
        are excluded from the exported state.
    output_filename : str or pathlib.Path
        Destination HTML path. Existing contents are replaced.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for a trusted internal call.

    Returns
    -------
    None
        The selected viewer and required widget resources are written to disk.

    Raises
    ------
    ArgumentError
        If the viewer or output path does not satisfy the argument contract.
    LibraryNotFoundError
        If the optional NGLView provider is unavailable.
    OSError
        If the destination cannot be written. Temporary serialization state is
        cleared before the exception propagates.

    Notes
    -----
    All coordinate structures exposed by the viewer are serialized through
    NGLView's existing resource preparation, which uses angstroms. The shared
    color registry and the requested viewer's active GUI theme are included
    alongside its widget dependencies.
    The private NGLView serialization hooks used here have matching contracts
    in the supported 3.0.4 baseline and the received 4.0.1 provider.

    Examples
    --------
    >>> import tempfile
    >>> from pathlib import Path
    >>> import molsysmt as msm
    >>> view = msm.view(msm.systems['Trp-Cage']['1l2y.pdb'],
    ...                 viewer='NGLView', structure_indices=[0])
    >>> with tempfile.TemporaryDirectory() as directory:
    ...     output = Path(directory) / 'molecular-view.html'
    ...     write_html(view, output)
    ...     print(output.is_file())
    True
    >>> view.close()

    .. versionadded:: 1.0.0
    """

    from ipywidgets import embed
    from nglview import NGLWidget
    from nglview.color import ColormakerRegistry

    from molsysmt._private.smonitor import ArgumentError
    from molsysmt.form.nglview_NGLWidget import get_n_structures_from_system

    if not isinstance(view, NGLWidget):
        raise ArgumentError(
            "view",
            value=view,
            message="view must be an nglview.NGLWidget for NGLView HTML export.",
        )

    n_structures = get_n_structures_from_system(view)
    views = [ColormakerRegistry, view]
    # The GUI theme is not a synchronized widget reference in supported NGLView
    # versions. Use this viewer's theme, rather than a global last-created one.
    theme = getattr(view, "_widget_theme", None)
    if theme is not None:
        views.insert(0, theme)
    resources = (
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/'
        'jqueryui/1.12.0/jquery-ui.css">\n'
        '<link rel="stylesheet" href="https://use.fontawesome.com/releases/'
        'v5.15.4/css/all.css">\n'
    )
    # NGLView's write_html does not accept an explicit state. Prepare only the
    # requested view, then use ipywidgets' supported dependency-limited embedding.
    try:
        view._set_serialization(frame_range=(0, n_structures))
        state = embed.dependency_state(views)
        snippet = resources + embed.embed_snippet(views, state=state)
        html = embed.html_template.format(title="nglview-embed", snippet=snippet)
        Path(output_filename).write_text(html, encoding="utf-8")
    finally:
        view._unset_serialization()
