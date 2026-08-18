from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

@arg_digest()
def set_color_by_value(view, values, element='group', selection='all', cmap='bwr_r',
        min_value=None, mid_value=None, max_value=None, representation='cartoon', syntax='MolSysMT'):
    """
    Adding a new representation colored by a color scale.

    A new representation can be added to an NGL view (NGLWidget) with elements colored by a list of values and a color map.


    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer instance.
    values : object
        Argument values.
    element : str, default='group'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    cmap : object, default='bwr_r'
        Argument cmap.
    min_value : object, default=None
        Argument min_value.
    mid_value : object, default=None
        Argument mid_value.
    max_value : object, default=None
        Argument max_value.
    representation : object, default='cartoon'
        Argument representation.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').

    Returns
    -------
    None
        The method modifies an nglview.NGLWidget object including the new representation.


    Notes
    -----

    Have a look to the `YYY`_.

    .. YYY:
       https://uibcdf.org/molsysmt

    See Also
    --------
    :func:`molsysmt.basic.view`, :func:`molsysmt.basic.select`


    Examples
    --------
    >>> import molsysmt as msm
    >>> from matplotlib.pyplot import colormaps
    >>> molecular_system = msm.convert('181L', selection='molecule_type=="protein"')
    >>> charge_residues = msm.physchem.charge(molecular_system, element='group', definition='physical_pH7') ￼
    >>> view = msm.view(molecular_system)
    >>> view.clear()
    >>> msm.thirds.nglview.color_by_value(view, charge_residues)
    >>> view
    """

    from nglview.color import _ColorScheme
    from molsysmt.basic import select
    from matplotlib.colors import Normalize, to_hex

    if min_value is None:
        min_value = min(values)
    if max_value is None:
        max_value = max(values)
    if mid_value is not None:
        l_max = abs(max_value-mid_value)
        l_min = abs(mid_value-min_value)
        l = max(l_max, l_min)
        min_value = mid_value - l
        max_value = mid_value + l

    norm = Normalize(vmin=min_value,vmax=max_value)

    if element=='group':
        elements_selection = select(view, element='group', selection=selection, syntax=syntax, to_syntax='NGLView')
        scheme = _ColorScheme([[to_hex(cmap(norm(ii))), jj] for ii,jj in zip(values, elements_selection.split(' '))], label='user')
    elif element=='atom':
        elements_selection = select(view, element='atom', selection=selection, syntax=syntax, to_syntax='NGLView')
        scheme = _ColorScheme([[to_hex(cmap(norm(ii))), '@'+jj] for ii,jj in zip(values, elements_selection[1:].split(','))], label='user')
    else:
        from molsysmt._private.smonitor import InternalAlgorithmError; raise InternalAlgorithmError(reason="NGLView helper reached an unexpected state.", caller=None)

    if representation=='surface':
        view.add_surface(selection=elements_selection, color=scheme)
    elif representation=='cartoon':
        view.add_cartoon(selection=elements_selection, color=scheme)
    elif representation=='licorice':
        view.add_licorice(selection=elements_selection, color=scheme)
    elif representation=='ball_and_stick':
        view.add_ball_and_stick(selection=elements_selection, color=scheme)

    pass
