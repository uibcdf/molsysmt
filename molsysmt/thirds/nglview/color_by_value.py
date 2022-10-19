from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md



@digest()
def color_by_value(view, values, element='group', selection='all', cmap=None,
        min_value=None, max_value=None, representation='cartoon', syntax='MolSysMT'):

    from nglview.color import _ColorScheme
    from molsysmt.basic import select
    from matplotlib.colors import Normalize, to_hex

    if element=='group':
        elements_selection = select(view, element='group', selection=selection, syntax=syntax, to_syntax='NGLview')
    else:
        raise ValueError()

    if min_value is None:
        min_value = min(values)
    if max_value is None:
        max_value = max(values)


    norm = Normalize(vmin=min_value,vmax=max_value)
    scheme = _ColorScheme([[to_hex(cmap(norm(ii))), jj] for ii,jj in zip(values, elements_selection.split(' '))], label='user')
    if representation=='surface':
        view.add_surface(selection=elements_selection, color=scheme)
    elif representation=='cartoon':
        view.clear()
        view.add_cartoon(selection=elements_selection, color=scheme)

    pass
