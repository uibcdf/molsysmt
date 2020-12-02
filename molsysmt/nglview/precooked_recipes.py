
# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

def standardize_view (view, atom_indices='all', frame_indices='all'):

    from molsysmt import select, get

    if atom_indices is not 'all':
        string_atom_indices = '@'+','.join(map(str, atom_indices))
    else:
        string_atom_indices = 'all'

    sel_cartoon = select(view, selection='molecule_type in ["protein","dna", "rna"]', mask=atom_indices, to_syntaxis='NGLview')
    sel_balls = select(view, selection='molecule_type in ["ion"]', mask=atom_indices, to_syntaxis='NGLview')
    sel_licorice = select(view, selection='molecule_type in ["peptide", "lipid","small_molecule"]', mask=atom_indices, to_syntaxis='NGLview')
    sel_water = select(view, selection='molecule_type in ["water"]', mask=atom_indices, to_syntaxis='NGLview')
    n_waters = get(view, target="system", n_waters=True)

    view.clear()
    view.add_cartoon(selection=sel_cartoon)
    view.add_licorice(selection=sel_licorice)
    view.add_ball_and_stick(selection=sel_balls)
    if n_waters<100:
        view.add_licorice(selection=sel_water)
    view.center(selection=string_atom_indices)

    pass

def show_water_as_transparent_surface(view, atom_indices='all', frame_indices='all'):

    if atom_indices is not 'all':
        string_atom_indices = '@'+','.join(map(str, atom_indices))
    else:
        string_atom_indices = 'all'

    string_atom_indices = string_atom_indices+' and water'
    view.add_surface(selection=string_atom_indices, opacity=0.3)

    pass

def show_water_as_licorice(view, atom_indices='all', frame_indices='all'):

    if atom_indices is not 'all':
        string_atom_indices = '@'+','.join(map(str, atom_indices))
    else:
        string_atom_indices = 'all'

    string_atom_indices = string_atom_indices+' and water'
    view.add_licorice(selection=string_atom_indices)

    pass

def show_colored_surface_by_scalar_residue_values(view, values, selection='all', cmap=None, vmin=None, vmax=None):

    from nglview.color import _ColorScheme
    from molsysmt import select
    from matplotlib.colors import Normalize, to_hex

    groups_selection = select(view, target='group', selection=selection, to_syntaxis='NGLview')

    if vmin is None:
        vmin = min(values)
    if vmax is None:
        vmax = max(values)

    norm = Normalize(vmin=vmin,vmax=vmax)
    scheme = _ColorScheme([[to_hex(cmap(norm(ii))), jj] for ii,jj in zip(values, groups_selection.split(' '))], label='user')
    view.add_surface(selection='protein', color=scheme)

    pass

def show_colored_cartoon_by_scalar_residue_values(view, values, selection='all', cmap=None, vmin=None, vmax=None):

    from nglview.color import _ColorScheme
    from molsysmt import select

    groups_selection = select(view, target='group', selection=selection, to_syntaxis='NGLview')

    if vmin is None:
        vmin = min(values)
    if vmax is None:
        vmax = max(values)

    norm = Normalize(vmin=vmin,vmax=vmax)
    scheme = _ColorScheme([[to_hex(cmap(norm(ii))), jj] for ii,jj in zip(values, groups_selection.split(' '))], label='user')
    view.add_cartoon(selection='protein', color=scheme)

    # It can also be done as:
    # nv.color.ColormakerRegistry.add_scheme('buried_factors',[['#'+ii[2:],str(jj)] for ii,jj in zip(colors, range(706))])
    # view.add_cartoon(selection='protein', color='buried_factors')

    pass

def add_gui(view):

    view.gui_style = 'ngl'

    pass
