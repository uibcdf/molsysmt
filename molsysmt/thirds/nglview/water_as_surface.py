from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

@digest()
def water_as_surface(view, opacity=0.3):

    view.add_surface(selection='water', opacity=opacity)

    pass

