from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

@digest()
def set_color(view, color, selection='all', syntax='MolSysMT'):

    from molsysmt.basic import select

    atoms_selection = select(view, element='atom', selection=selection, syntax=syntax, to_syntax='NGLView')
    view.update_representation(component=0, selection=atoms_selection, color=color)

    pass
