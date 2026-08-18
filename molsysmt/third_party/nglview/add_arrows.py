from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

@arg_digest()
def add_arrows(view, origin=None, end=None, vectors=None,
               color='#808080', radius='0.2 angstroms'):
    """
    Adding 3D arrows between start and end coordinate points in NGLWidget.


    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer instance.
    origin : numpy.ndarray, list, or tuple, default=None
        Origin coordinates vector for arrows.
    end : object, default=None
        Argument end.
    vectors : numpy.ndarray, list, or tuple, default=None
        Direction and magnitude vectors array.
    color : object, default='#808080'
        Argument color.
    radius : object, default='0.2 angstroms'
        Argument radius.

    .. versionadded:: 1.0.0
    """

    from molsysmt import get
    from molsysmt._private.colors import color_to_list_of_colors
    from molsysmt._private.input_arguments import can_be_selection

    if can_be_selection(origin):
        origin = get(view, element='atom', selection=origin, coordinates=True)
    if can_be_selection(end):
        end = get(view, element='atom', selection=end, coordinates=True)

    if (origin is not None) and (end is not None):
        origin = puw.get_value(origin, to_unit='angstroms')
        end = puw.get_value(end, to_unit='angstroms')
        if origin.ndim == 3: origin = origin[0]
        if end.ndim == 3: end = end[0]
    elif (origin is not None) and (vectors is not None):
        origin = puw.get_value(origin, to_unit='angstroms')
        vectors = puw.get_value(vectors, to_unit='angstroms')
        if origin.ndim == 3: origin = origin[0]
        if vectors.ndim == 3: vectors = vectors[0]
        if origin.shape[0]!=vectors.shape[0] and vectors.shape[0]==1:
            vectors = np.tile(vectors, (origin.shape[0], 1))
        end = origin + vectors
    elif (end is not None) and (vectors is not None):
        end = puw.get_value(end, to_unit='angstroms')
        vectors = puw.get_value(vectors, to_unit='angstroms')
        if end.ndim == 3: end = end[0]
        if vectors.ndim == 3: vectors = vectors[0]
        if origin.shape[0]!=vectors.shape[0] and vectors.shape[0]==1:
            vectors = np.tile(vectors, (origin.shape[0], 1))
        origin = end - vectors
    else:
        from molsysmt._private.smonitor import InternalAlgorithmError; raise InternalAlgorithmError(reason="NGLView helper reached an unexpected state.", caller=None)

    radius = puw.get_value(radius, to_unit='angstroms')
    n_arrows=origin.shape[0]

    list_of_colors = color_to_list_of_colors(color, n_arrows, form='rgb')

    for ii in range(n_arrows):

        kwargs = {'position1':origin[ii].tolist(),
                  'position2':end[ii].tolist(),
                  'color': list_of_colors[ii],
                  'radius': [radius]}

        # Use nglview's remote_call to queue the buffer safely regardless of load state.
        view._remote_call(
            "addBuffer",
            target="Widget",
            args=["arrow"],
            kwargs=kwargs,
            fire_embed=True,
        )
