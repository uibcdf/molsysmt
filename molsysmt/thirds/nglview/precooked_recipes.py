from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

@digest()
def standardize_view (view, atom_indices='all', structure_indices='all'):

    view.clear()

    from molsysmt.basic import select, get, convert
    from molsysmt.build import is_solvated

    if not is_all(atom_indices):
        string_atom_indices = '@'+','.join(map(str, atom_indices))
    else:
        string_atom_indices = 'all'

    tmp_topology = convert(view, to_form='molsysmt.Topology')

    mask_string = ''
    if not is_all(atom_indices):
        mask_string = ' and atom_index in @atom_indices'

    sel_cartoon = select(tmp_topology, selection='molecule_type in ["protein", "dna", "rna"]'+mask_string, to_syntax='NGLView')
    sel_balls = select(tmp_topology, selection='molecule_type in ["ion"]'+mask_string, to_syntax='NGLView')
    sel_licorice = select(tmp_topology, selection='molecule_type in ["lipid", "small molecule"]'+mask_string, to_syntax='NGLView')

    peptide_indices = select(tmp_topology, selection='molecule_type=="peptide"', element='molecule')
    peptides_to_cartoon = []
    peptides_to_licorice = []
    for peptide_index in peptide_indices:
        n_groups = get(tmp_topology, element='molecule', selection=peptide_index, n_groups=True)[0]
        if n_groups >7: # two turns of alpha-helix
            peptides_to_cartoon.append(peptide_index)
        else:
            peptides_to_licorice.append(peptide_index)

    sel_peptides_cartoon = select(tmp_topology, selection='molecule_index in @peptides_to_cartoon'+mask_string, to_syntax='NGLView')
    sel_peptides_licorice = select(tmp_topology, selection='molecule_index in @peptides_to_licorice'+mask_string, to_syntax='NGLView')

    view.add_cartoon(selection=sel_cartoon)
    view.add_cartoon(selection=sel_peptides_cartoon)
    view.add_licorice(selection=sel_licorice, radius=0.4)
    view.add_licorice(selection=sel_peptides_licorice, radius=0.4)
    view.add_ball_and_stick(selection=sel_balls)

    view.center(selection=string_atom_indices)

    pass

@digest()
def show_water_as_transparent_surface(view, atom_indices='all', structure_indices='all'):

    if not is_all(atom_indices):
        string_atom_indices = '@'+','.join(map(str, atom_indices))
    else:
        string_atom_indices = 'all'

    string_atom_indices = string_atom_indices+' and water'
    view.add_surface(selection=string_atom_indices, opacity=0.3)

    pass

@digest()
def show_water_as_licorice(view, atom_indices='all', structure_indices='all'):

    if not is_all(atom_indices):
        string_atom_indices = '@'+','.join(map(str, atom_indices))
    else:
        string_atom_indices = 'all'

    string_atom_indices = string_atom_indices+' and water'
    view.add_licorice(selection=string_atom_indices)

    pass


@digest()
def show_system_as_transparent_surface(view, atom_indices='all', structure_indices='all'):

    view.add_surface(selection='all', opacity=0.3, color='lightblue')

    pass


@digest()
def add_gui(view):

    view.gui_style = 'ngl'

    pass
