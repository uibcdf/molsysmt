
# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

def standardize_view (view, atom_indices='all', frame_indices='all'):

    if atom_indices is not 'all':
        string_atom_indices = '@'+','.join(map(str, atom_indices))
    else:
        string_atom_indices = 'all'

    sel_cartoon = string_atom_indices+' and (protein or nucleic)'
    sel_balls = string_atom_indices+' and ion'
    sel_licorice = string_atom_indices+' and (ligand or hetero)'

    view.clear()
    view.add_cartoon(selection=sel_cartoon)
    view.add_licorice(selection=sel_licorice)
    view.add_ball_and_stick(selection=sel_licorice)
    view.center(selection=string_atom_indices)

    # water is not shown

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

def show_colored_surface_by_scalar_residue_values(view, values, color_min=[255,255,255],
                                                  color_max=[255,0,0], value_min=None,
                                                  value_max=None):

    from nglview.color import _ColorScheme
    from molsysmt.utils.color import colorscale2hex

    colors = colorscale2hex(values, color_min=color_min, color_max=color_max, value_min=value_min, value_max=value_max)
    scheme = _ColorScheme([['#'+ii[2:],str(jj)] for ii,jj in zip(colors, range(len(values)))], label='user')
    view.add_surface(selection='protein', color=scheme)

    pass

def show_colored_cartoon_by_scalar_residue_values(view, values, color_min=[255,255,255],
                                                  color_max=[255,0,0], value_min=None,
                                                  value_max=None):

    from nglview.color import _ColorScheme
    from molsysmt.utils.color import colorscale2hex

    colors = colorscale2hex(values, color_min=color_min, color_max=color_max, value_min=value_min, value_max=value_max)
    scheme = _ColorScheme([['#'+ii[2:],str(jj)] for ii,jj in zip(colors, range(len(values)))], label='user')
    view.add_cartoon(selection='protein', color=scheme)

    # It can also be done as:
    # nv.color.ColormakerRegistry.add_scheme('buried_factors',[['#'+ii[2:],str(jj)] for ii,jj in zip(colors, range(706))])
    # view.add_cartoon(selection='protein', color='buried_factors')

    pass

def add_gui(view):

    view.gui_style = 'ngl'

    pass
