from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all, is_iterable
from molsysmt._private.colors import color_to_list_of_colors, get_list_of_colors_from_values
from molsysmt import pyunitwizard as puw
import numpy as np


@digest()
def add_cylinders(view, bottom=None, top=None, vectors=None, color='#808080', color_2=None, radius='0.1 angstroms',
        color_values=None, min_color_value=None, mid_color_value=None, max_color_value=None,
        color_values_scale='linear', colormap='bwr', color_values_2=None, min_color_value_2=None,
        mid_color_value_2=None, max_color_value_2=None, color_values_scale_2=None, colormap_2=None):

    """Adding cylinders to a view.

    Cylinders can be added to an NGL view (NGLWidget).

    Parameters
    ----------

    view: nglview.NGLWidget
       A view of the molecular system as an nglview.NGLWidget native object.

    start: Quantity (value:numpy.ndarray, dimensionality:['L']=1)
       Positions of the origin points for the set of cylinders. A quantity with length
       dimensions is required (['L']=1), the value must be a numpy ndarray with shape [n_cylinders,
       3] (n_cylinders is the number of arrows to be added).

    end: Quantity (value:numpy.ndarray, dimensionality:['L']=1)
       Positions of the end points for the set of cylinders. A quantity with length
       dimensions is required (['L']=1), the value must be a numpy ndarray with shape [n_cylinders,
       3] (n_cylinders is the number of arrows to be added).

    color: list, tuple, string default='#808080'
       HEX or RGB color code of the first half of the cylinder.

    color2: list, tuple, string default='#808080'
       HEX or RGB color code of the first half of the cylinder.

    radius: Quantity (value:float, dimensionality:['L']=1), default='0.2 angstroms'
       Radius of the cylinder.

    Returns
    -------
    None
        The method modifies an nglview.NGLWidget object to add a list of arrows.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import pyunitwizard as puw
    >>> import nglview as nv
    >>> view = nv.NGLWidget()
    >>> start = puw.quantity([[0,0,0], [0,5,0]], 'angstroms')
    >>> end = puw.quantity([[10,0,0], [0,10,0]], 'angstroms')
    >>> msm.thirds.nglview.add_cylinders(view, start, end, color='#ff0000', color_2='#0000ff', radius='0.2 angstroms')
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

    from molsysmt import get
    from molsysmt._private.input_arguments import can_be_selection

    if can_be_selection(bottom):
        bottom = get(view, element='atom', selection=bottom, coordinates=True)
    if can_be_selection(top):
        top = get(view, element='atom', selection=top, coordinates=True)

    if (bottom is not None) and (top is not None):
        bottom = puw.get_value(bottom[0], to_unit='angstroms')
        top = puw.get_value(top[0], to_unit='angstroms')
    elif (bottom is not None) and (vectors is not None):
        bottom = puw.get_value(bottom[0], to_unit='angstroms')
        vectors = puw.get_value(vectors[0], to_unit='angstroms')
        if bottom.shape[0]!=vectors.shape[0] and vectors.shape[0]==1:
            vectors = np.tile(vectors, (bottom.shape[0], 1))
        top = bottom + vectors
    elif (top is not None) and (vectors is not None):
        top = puw.get_value(top[0], to_unit='angstroms')
        vectors = puw.get_value(vectors[0], to_unit='angstroms')
        if bottom.shape[0]!=vectors.shape[0] and vectors.shape[0]==1:
            vectors = np.tile(vectors, (bottom.shape[0], 1))
        bottom = top - vectors
    else:
        raise ValueError()


    n_cylinders=bottom.shape[0]

    ngl_start = bottom
    ngl_end = top
    ngl_radius = puw.get_value(radius, to_unit='angstroms')

    if not is_iterable(ngl_radius):
        ngl_radius = [ngl_radius for ii in range(n_cylinders)]

    if color_values is not None:
        ngl_color = get_list_of_colors_from_values(color_values, min_value=min_color_value,
                mid_value=mid_color_value, max_value=max_color_value, scale=color_values_scale,
                colormap=colormap, form='rgb')
    else:
        ngl_color = color_to_list_of_colors(color, n_cylinders, 'rgb')

    if color_values_2 is not None:
        if colormap_2 is None:
            colormap_2 = colormap
        if color_values_scale_2 is None:
            color_values_scale_2 = color_values_scale
        ngl_color_2 = get_list_of_colors_from_values(color_values_2, min_value=min_color_value_2,
                mid_value=mid_color_value_2, max_value=max_color_value_2, scale=color_values_scale_2,
                colormap=colormap_2, form='rgb')
    else:
        if color_2 is None:
            ngl_color_2 = ngl_color
        else:
            ngl_color_2 = color_to_list_of_colors(color_2, n_cylinders, 'rgb')


    for ii in range(n_cylinders):

        kwargs = {'position1':ngl_start[ii].tolist(),
                  'position2':ngl_end[ii].tolist(),
                  'color': ngl_color[ii],
                  'color2': ngl_color_2[ii],
                  'radius': [ngl_radius[ii]]}

        msg = view._get_remote_call_msg("addBuffer",
                                        target="Widget",
                                        args=["cylinder"],
                                        kwargs=kwargs,
                                        fire_embed=True)

        def callback(widget, msg=msg):
            widget.send(msg)

        callback._method_name = 'addBuffer'
        callback._ngl_msg = msg

        if view.loaded:
            view._remote_call_thread.q.append(callback)
        else:
            view._ngl_displayed_callbacks_before_loaded.append(callback)

        view._ngl_msg_archive.append(msg)

    pass

