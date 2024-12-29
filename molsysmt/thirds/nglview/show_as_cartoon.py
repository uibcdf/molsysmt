from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md


@digest(form='nglview.NGLWidget')
def show_as_cartoon(view, selection='all', color='blue', skip_digestion=False):

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

    view.add_cartoon(selection=nglview_selection, color=color)

    pass

