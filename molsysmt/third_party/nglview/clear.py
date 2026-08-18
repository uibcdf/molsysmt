from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md


@arg_digest(form='nglview.NGLWidget')
def clear(view, skip_digestion=False):
    """
    Clearing all visual representations and components from an NGLWidget viewer.


    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer instance.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """

    view.clear_representations()

    pass

