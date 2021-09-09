
# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

def standardize_view (view, atom_indices='all', frame_indices='all'):

    from molsysmt.basic import select, get, convert
    from molsysmt.build import is_solvated


    if atom_indices is not 'all':
        string_atom_indices = '@'+','.join(map(str, atom_indices))
    else:
        string_atom_indices = 'all'

    tmp_topology = convert(view, to_form='molsysmt.Topology')

    sel_cartoon = select(tmp_topology, selection='molecule_type in ["protein", "dna", "rna"]', mask=atom_indices, to_syntaxis='NGLview')
    sel_balls = select(tmp_topology, selection='molecule_type in ["ion"]', mask=atom_indices, to_syntaxis='NGLview')
    sel_licorice = select(tmp_topology, selection='molecule_type in ["lipid", "small molecule"]', mask=atom_indices, to_syntaxis='NGLview')

    peptide_indices = select(tmp_topology, selection='molecule_type=="peptide"', target='molecule')
    peptides_to_cartoon = []
    peptides_to_licorice = []
    for peptide_index in peptide_indices:
        n_aminoacids = get(tmp_topology, target='molecule', indices=peptide_index, n_groups=True)[0]
        if n_aminoacids > 4:
            peptides_to_cartoon.append(peptide_index)
        else:
            peptides_to_licorice.append(peptide_index)
    sel_peptides_cartoon = select(tmp_topology, selection='molecule_index in @peptides_to_cartoon', mask=atom_indices, to_syntaxis='NGLview')
    sel_peptides_licorice = select(tmp_topology, selection='molecule_index in @peptides_to_licorice', mask=atom_indices, to_syntaxis='NGLview')

    view.clear()
    view.add_cartoon(selection=sel_cartoon)
    view.add_cartoon(selection=sel_peptides_cartoon)
    view.add_licorice(selection=sel_licorice, radius=0.4)
    view.add_licorice(selection=sel_peptides_licorice, radius=0.4)
    view.add_ball_and_stick(selection=sel_balls)

    n_waters = get(view, target="system", n_waters=True)
    n_selected_waters = get(view, target="system", n_waters=True)
    solvated = is_solvated(view)

    if (not solvated) or (n_selected_waters<n_waters):
        sel_water = select(tmp_topology, selection='molecule_type in ["water"]', mask=atom_indices, to_syntaxis='NGLview')
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

def show_system_as_transparent_surface(view, atom_indices='all', frame_indices='all'):

    view.add_surface(selection='all', opacity=0.3, color='lightblue')

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
    from molsysmt.basic import select
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
    from molsysmt.basic import select

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
