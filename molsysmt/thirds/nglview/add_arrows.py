from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

@digest()
def add_arrows(view, arrows, origin=None, selection=None, color='#808080', radius='0.2 angstroms'):
    """Adding arrows to a view.

    A list of arrows can be added to an NGL view (NGLWidget).

    Parameters
    ----------

    view: nglview.NGLWidget
       A view of the molecular system as an nglview.NGLWidget native object.

    coordinates: Quantity (value:numpy.ndarray, dimensionality:['L']=1)
       Positions of the points of origin for the set of arrows. A quantity with length dimensions is required (['L']=1), the value must be a numpy ndarray with shape [n_arrows, 3] (n_arrows is the number of arrows to be added).

    arrows: Quantity (value:numpy.ndarray, dimensionality:['L']=1)
       Vectors to be added as arrows. A quantity with length dimensions is required (['L']=1), the value must be a numpy ndarray with shape [n_arrows, 3] (n_arrows is the number of arrows to be added).

    color: list, tuple, string default='#808080'
       HEX or RGB color code of the arrows.

    radius: Quantity (value:float, dimensionality:['L']=1), default='0.2 angstroms'
       Radius of the arrows.

    Returns
    -------
    None
        The method modifies an nglview.NGLWidget object to add a list of arrows.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import pyunitwizard as puw
    >>> import numpy as np
    >>> molecular_system = msm.convert('181L', selection='molecule_type=="protein"')
    >>> coordinates = msm.get(molecular_system, element='atom', selection='atom_name=="CA"', coordinates=True)
    >>> arrows = puw.quantity(np.ones([coordinates.shape[0],3]), 'angstroms')
    >>> view = msm.view(molecular_system)
    >>> msm.thirds.add_arrows(view, arrows, origin=coordinates)
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
    from molsysmt._private.colors import color_to_list_of_colors

    if origin is not None:
        coordinates = puw.get_value(origin[0], to_unit='angstroms')
    elif selection is not None:
        from molsysmt import get
        coordinates = get(view, element='atom', selection=selection, coordinates=True)
        coordinates = puw.get_value(coordinates[0], to_unit='angstroms')
    else:
        raise ValueError()

    arrows = puw.get_value(arrows[0], to_unit='angstroms')
    radius = puw.get_value(radius, to_unit='angstroms')

    n_arrows=coordinates.shape[0]
    end_arrows = coordinates+arrows

    list_of_colors = color_to_list_of_colors(color, n_arrows, form='rgb')

    for ii in range(n_arrows):
    
        kwargs = {'position1':coordinates[ii].tolist(),
                  'position2':end_arrows[ii].tolist(),
                  'color': list_of_colors[ii],
                  'radius': [radius]}
                        
        msg = view._get_remote_call_msg("addBuffer",
                                        target="Widget",
                                        args=["arrow"],
                                        kwargs=kwargs,
                                        fire_embed=True)

        def callback(widget, msg=msg):
            widget.send(msg)

        callback._method_name = 'addBuffer'
        callback._ngl_msg = msg

        view._ngl_displayed_callbacks_before_loaded.append(callback)

        view._ngl_msg_archive.append(msg)

    pass

