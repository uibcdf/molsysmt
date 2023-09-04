from molsysmt._private.exceptions import NotImplementedMethodError


def select(item, selection):

    from . import convert, get_form

    form_in = get_form(item)

    if form_in == 'MDAnalysis.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='MDAnalysis.Topology')

    tmp_atomgroup = tmp_item.select_atoms(selection)
    atom_indices = tmp_atomgroup.atoms.ids
    del(tmp_atomgroup)

    return atom_indices

def indices_to_selection(molecular_system, indices, element='atom'):

    raise NotImplementedMethodError

