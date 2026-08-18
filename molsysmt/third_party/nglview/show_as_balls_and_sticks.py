from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md


@arg_digest(form='nglview.NGLWidget')
def show_as_balls_and_sticks(view, selection='all', skip_digestion=False):
    """
    Adding ball-and-stick representation for selected elements in NGLWidget.

    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer.
    selection : str or list of int, default='all'
        Selection of atoms to represent.
    color : str or list, optional
        Color name, hex code, or scheme.
    opacity : float, optional
        Opacity value between 0.0 and 1.0.

    .. versionadded:: 1.0.0
    """

    from molsysmt import select

    nglview_selection=None

    if isinstance(selection, str):
        if selection=='molecule_type=="water"' or selection=='group_type=="water"':
            nglview_selection='water'
        if selection=='molecule_type=="ion"' or selection=='group_type=="ion"':
            nglview_selection='ion'

    if nglview_selection is None:
        nglview_selection = select(view, element='atom', selection=selection, to_syntax='NGLView',
                                  skip_digestion=True)

    view.add_ball_and_stick(selection=nglview_selection)

    pass

