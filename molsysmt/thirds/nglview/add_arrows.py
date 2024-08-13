from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

@digest()
def add_arrows(view, origin=None, end=None, vectors=None,
               color='#808080', radius='0.2 angstroms'):
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
    >>> vectors = puw.quantity(np.ones([coordinates.shape[0],3]), 'angstroms')
    >>> view = msm.view(molecular_system)
    >>> msm.thirds.add_arrows(view, origin=coordinates, vectors=arrows)
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
    from molsysmt._private.input_arguments import can_be_selection

    if can_be_selection(origin):
        origin = get(view, element='atom', selection=origin, coordinates=True)
    if can_be_selection(end):
        end = get(view, element='atom', selection=end, coordinates=True)

    if (origin is not None) and (end is not None):
        origin = puw.get_value(origin[0], to_unit='angstroms')
        end = puw.get_value(end[0], to_unit='angstroms')
    elif (origin is not None) and (vectors is not None):
        origin = puw.get_value(origin[0], to_unit='angstroms')
        vectors = puw.get_value(vectors[0], to_unit='angstroms')
        if origin.shape[0]!=vectors.shape[0] and vectors.shape[0]==1:
            vectors = np.tile(vectors, (origin.shape[0], 1))
        end = origin + vectors
    elif (end is not None) and (vectors is not None):
        end = puw.get_value(end[0], to_unit='angstroms')
        vectors = puw.get_value(vectors[0], to_unit='angstroms')
        if origin.shape[0]!=vectors.shape[0] and vectors.shape[0]==1:
            vectors = np.tile(vectors, (origin.shape[0], 1))
        origin = end - vectors
    else:
        raise ValueError()

    radius = puw.get_value(radius, to_unit='angstroms')
    n_arrows=origin.shape[0]

    list_of_colors = color_to_list_of_colors(color, n_arrows, form='rgb')

    for ii in range(n_arrows):
    
        kwargs = {'position1':origin[ii].tolist(),
                  'position2':end[ii].tolist(),
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

