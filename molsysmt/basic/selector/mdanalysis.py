from molsysmt._private.exceptions import NotImplementedMethodError

def select(molecular_system, selection='all', structure_indices='all'):

    from . import convert, get_form

    form_in = get_form(molecular_system)

    if form_in == 'MDAnalysis.Topology':
        tmp_item = molecular_system
    else:
        tmp_item = convert(molecular_system, to_form='MDAnalysis.Topology')

    tmp_atomgroup = tmp_item.select_atoms(selection)
    atom_indices = tmp_atomgroup.atoms.ids
    del(tmp_atomgroup)

    return atom_indices

def indices_to_selection(molecular_system, indices, element='atom'):

    raise NotImplementedMethodError

