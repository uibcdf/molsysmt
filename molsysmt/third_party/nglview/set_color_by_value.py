from molsysmt._private.argdigest import arg_digest

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md


@arg_digest()
def set_color_by_value(
    view,
    values,
    element="group",
    selection="all",
    cmap="bwr_r",
    min_value=None,
    mid_value=None,
    max_value=None,
    representation="cartoon",
    syntax="MolSysMT",
):
    """Adding an NGLView representation colored by numerical values.

    Map one value per selected atom or group through a Matplotlib colormap.
    The view is modified in place; existing representations are retained.

    Parameters
    ----------
    view : nglview.NGLWidget
        Target NGLView widget. Create it with ``msm.view(molsys, viewer='NGLView')``.
    values : sequence of float
        Numerical values aligned with the selected atoms or groups in the order
        returned by ``msm.select(view, element=element, selection=selection)``.
        Express all values and limits on the same numerical scale.
    element : str, default='group'
        Element whose values are colored: 'atom' or 'group'.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection of atoms or groups whose values are supplied.
    cmap : str or matplotlib.colors.Colormap, default='bwr_r'
        Registered Matplotlib colormap name or colormap object.
    min_value : float or none, default=None
        Lower normalization limit. If None, use the minimum supplied value.
    mid_value : float or none, default=None
        Optional center of the scale. If supplied, expand both normalization
        limits symmetrically around it, retaining the more distant endpoint.
    max_value : float or none, default=None
        Upper normalization limit. If None, use the maximum supplied value.
    representation : str, default='cartoon'
        Representation to add: 'cartoon', 'surface', 'licorice' or 'ball_and_stick'.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate ``selection``.

    Returns
    -------
    none
        The widget receives a new representation with the requested color scheme.

    Notes
    -----
    This helper targets NGLView explicitly. MolSysMT's default viewer is
    MolSysViewer. Compute values for the same selection and element used here;
    passing an entire-system value array to a selected subset can misalign colors.
    Python examples verify representation submission, not browser rendering.

    See Also
    --------
    molsysmt.basic.view
        Create a view with an explicit viewer backend.
    molsysmt.basic.select
        Obtain the selected indices used to align numerical values.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'],
    ...                      selection='molecule_type=="protein"')
    >>> values = msm.physchem.get_charge(molsys, element='group',
    ...                                  definition='physical_pH7')
    >>> view = msm.view(molsys, viewer='NGLView')
    >>> view.clear()
    >>> msm.third_party.nglview.set_color_by_value(view, values) is None
    True

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_NGLView_Set_color_by_value` for a usage example.

    .. versionadded:: 1.0.0
    """

    from matplotlib.colors import Normalize, to_hex
    from nglview.color import _ColorScheme

    from molsysmt.basic import select

    if min_value is None:
        min_value = min(values)
    if max_value is None:
        max_value = max(values)
    if mid_value is not None:
        l_max = abs(max_value - mid_value)
        l_min = abs(mid_value - min_value)
        half_range = max(l_max, l_min)
        min_value = mid_value - half_range
        max_value = mid_value + half_range

    norm = Normalize(vmin=min_value, vmax=max_value)

    if element == "group":
        elements_selection = select(
            view,
            element="group",
            selection=selection,
            syntax=syntax,
            to_syntax="NGLView",
        )
        scheme = _ColorScheme(
            [
                [to_hex(cmap(norm(ii))), jj]
                for ii, jj in zip(values, elements_selection.split(" "))
            ],
            label="user",
        )
    elif element == "atom":
        elements_selection = select(
            view,
            element="atom",
            selection=selection,
            syntax=syntax,
            to_syntax="NGLView",
        )
        scheme = _ColorScheme(
            [
                [to_hex(cmap(norm(ii))), "@" + jj]
                for ii, jj in zip(values, elements_selection[1:].split(","))
            ],
            label="user",
        )
    else:
        from molsysmt._private.smonitor import InternalAlgorithmError

        raise InternalAlgorithmError(
            reason="NGLView helper reached an unexpected state.", caller=None
        )

    if representation == "surface":
        view.add_surface(selection=elements_selection, color=scheme)
    elif representation == "cartoon":
        view.add_cartoon(selection=elements_selection, color=scheme)
    elif representation == "licorice":
        view.add_licorice(selection=elements_selection, color=scheme)
    elif representation == "ball_and_stick":
        view.add_ball_and_stick(selection=elements_selection, color=scheme)

    pass
