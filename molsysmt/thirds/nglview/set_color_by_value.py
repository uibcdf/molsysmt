from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

@digest()
def set_color_by_value(view, values, element='group', selection='all', cmap='bwr_r',
        min_value=None, max_value=None, representation='cartoon', syntax='MolSysMT'):
    """Adding a new representation colored by a color scale.

    A new representation can be added to an NGL view (NGLWidget) with elements colored by a list of values and a color map.

    Parameters
    ----------

    view: nglview.NGLWidget
       A view of the molecular system as an nglview.NGLWidget native object.

    values: list, tuple or numpy.ndarray
       List of values or magnitudes corresponding to each element to be encoded as a color.

    element: str, default='group'
       Element to be colored according to its value in the input argument `values`.

    selection: str, list, tuple or numpy.ndarray, default='all'
       Selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`).

    cmap: str, matplotlib.colors.LinearSegmentedColormap, default:'rwb'
       The name of the matplotlib colormap or a LineraSegemendedColormap native Python object of the MatPlotLib library.

    min_value: float, Quantity, default='None'
       Minimum value of the color scale. By default ('None'), the minimum of the input argument `values` is taken.

    max_value: float, Quantity, default='None'
       Maximum value of the color scale. By default ('None'), the maximum of the input argument `values` is taken.

    representation: str, default='cartoon'
       Representation type supported by NGLView: 'cartoon', 'licorice', 'surface', 'ball_and_stick'...

    syntax: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.basic.select`).

    Returns
    -------
    None
        The method modifies an nglview.NGLWidget object including the new representation.

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

    See Also
    --------
    :func:`molsysmt.basic.view`, :func:`molsysmt.basic.select`

    Notes
    -----

    Have a look to the `YYY`_.

    .. YYY:
       https://uibcdf.org/molsysmt


    """

    from nglview.color import _ColorScheme
    from molsysmt.basic import select
    from matplotlib.colors import Normalize, to_hex

    if min_value is None:
        min_value = min(values)
    if max_value is None:
        max_value = max(values)

    norm = Normalize(vmin=min_value,vmax=max_value)

    if element=='group':
        elements_selection = select(view, element='group', selection=selection, syntax=syntax, to_syntax='NGLView')
        scheme = _ColorScheme([[to_hex(cmap(norm(ii))), jj] for ii,jj in zip(values, elements_selection.split(' '))], label='user')
    elif element=='atom':
        elements_selection = select(view, element='atom', selection=selection, syntax=syntax, to_syntax='NGLView')
        scheme = _ColorScheme([[to_hex(cmap(norm(ii))), '@'+jj] for ii,jj in zip(values, elements_selection[1:].split(','))], label='user')
    else:
        raise ValueError()

    if representation=='surface':
        view.add_surface(selection=elements_selection, color=scheme)
    elif representation=='cartoon':
        view.add_cartoon(selection=elements_selection, color=scheme)
    elif representation=='licorice':
        view.add_licorice(selection=elements_selection, color=scheme)
    elif representation=='ball_and_stick':
        view.add_ball_and_stick(selection=elements_selection, color=scheme)

    pass
