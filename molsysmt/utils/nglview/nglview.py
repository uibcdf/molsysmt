
# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

def standardize_view (view, atom_indices=None, frame_indices=None):

    string_atom_indices = '@'+','.join(map(str, atom_indices))
    sel_cartoon = string_atom_indices+' and (protein or nucleic)'
    sel_balls = string_atom_indices+' and ion'
    sel_licorice = string_atom_indices+' and (ligand or hetero)'

    view.clear()
    view.add_cartoon(selection=sel_cartoon)
    view.add_licorice(selection=sel_licorice)
    view.add_ball_and_stick(selection=sel_licorice)
    view.center(selection=string_atom_indices)

    return view

def show_water_as_transparent_surface(view, atom_indices=None, frame_indices=None):

    string_atom_indices = '@'+','.join(map(str, atom_indices))+'and water'
    view.add_surface(selection='water', opacity=0.3)

    return view

def show_water_as_licorice(view, atom_indices=None, frame_indices=None):

    sel_water = '@'+','.join(map(str, atom_indices))+'and water'
    view.add_licorice(selection=sel_water)

    return view

