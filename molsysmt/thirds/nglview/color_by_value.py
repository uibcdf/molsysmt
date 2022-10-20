from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md



@digest()
def color_by_value(view, values, element='group', selection='all', cmap=None,
        min_value=None, max_value=None, representation='cartoon', syntax='MolSysMT'):

    from nglview.color import _ColorScheme
    from molsysmt.basic import select
    from matplotlib.colors import Normalize, to_hex

    if min_value is None:
        min_value = min(values)
    if max_value is None:
        max_value = max(values)

    norm = Normalize(vmin=min_value,vmax=max_value)

    if element=='group':
        elements_selection = select(view, element='group', selection=selection, syntax=syntax, to_syntax='NGLview')
        scheme = _ColorScheme([[to_hex(cmap(norm(ii))), jj] for ii,jj in zip(values, elements_selection.split(' '))], label='user')
    elif element=='atom':
        elements_selection = select(view, element='atom', selection=selection, syntax=syntax, to_syntax='NGLview')
        scheme = _ColorScheme([[to_hex(cmap(norm(ii))), '@'+jj] for ii,jj in zip(values, elements_selection[1:].split(','))], label='user')
    else:
        raise ValueError()
    
    if representation=='surface':
        view.add_surface(selection=elements_selection, color=scheme)
    elif representation=='cartoon':
        view.add_cartoon(selection=elements_selection, color=scheme)
    elif representation=='licorice':
        view.add_licorice(selection=elements_selection, color=scheme)
    elif representation=='ball_and_stick':
        view.add_ball_and_stick(selection=elements_selection, color=scheme)

    pass
