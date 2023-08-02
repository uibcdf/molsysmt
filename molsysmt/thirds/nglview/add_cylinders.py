from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from matplotlib.colors import to_rgb
from molsysmt import pyunitwizard as puw


#@digest()
def add_cylinders(view, start, end, color='#808080', color2='#808080', radius='0.2 angstroms'):
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
    >>> msm.thirds.nglview.add_cylinders(view, start, end, color='#ff0000', color2='#0000ff', radius='0.2 angstroms')
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

    if isinstance(color, str):

        color=to_rgb(color)

    if isinstance(color2, str):

        color2=to_rgb(color2)



    n_cylinders=start.shape[0]

    ngl_start = puw.get_value(start, to_unit='angstroms')
    ngl_end = puw.get_value(end, to_unit='angstroms')
    ngl_radius = puw.get_value(radius, to_unit='angstroms')
    ngl_color = color
    ngl_color2 = color2

    for ii in range(n_cylinders):

        kwargs = {'position1':ngl_start[ii].tolist(),
                  'position2':ngl_end[ii].tolist(),
                  'color': ngl_color,
                  'color2': ngl_color2,
                  'radius': [ngl_radius]}

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

