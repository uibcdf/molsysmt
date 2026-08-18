from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

@arg_digest()
def set_color(view, color, selection='all', syntax='MolSysMT'):
    """
    Setting uniform or custom color on representations in NGLWidget.

    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer.
    color : str, default='white'
        Color name or hex code.
    selection : str or list of int, default='all'
        Selection of atoms or components to color.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select

    atoms_selection = select(view, element='atom', selection=selection, syntax=syntax, to_syntax='NGLView')
    view.update_representation(component=0, selection=atoms_selection, color=color)

    pass
