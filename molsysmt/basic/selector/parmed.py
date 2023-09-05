from molsysmt._private.exceptions import NotImplementedMethodError

def select(item, selection):

    from . import convert, get_form
    from parmed.amber import AmberMask as _AmberMask

    form_in = get_form(item)

    if form_in == 'parmed.Structure':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='parmed.Structure')

    atom_indices = list(_AmberMask(item,selection).Selected())
    del(_AmberMask)

    return tmp_atom_indices

def indices_to_selection(molecular_system, indices, element='atom'):

    raise NotImplementedMethodError


