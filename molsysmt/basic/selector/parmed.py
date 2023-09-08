from molsysmt._private.exceptions import NotImplementedMethodError

def select(molecular_system, selection='all', structure_indices='all'):

    #from . import convert, get_form
    #from parmed.amber import AmberMask as _AmberMask

    #form_in = get_form(molecular_system)

    #if form_in == 'parmed.Structure':
    #    tmp_item = molecular_system
    #else:
    #    tmp_item = convert(molecular_system, to_form='parmed.Structure')

    #atom_indices = list(_AmberMask(item, selection).Selected())
    #del(_AmberMask)

    #return tmp_atom_indices

    raise NotImplementedMethodError

def indices_to_selection(molecular_system, indices, element='atom'):

    raise NotImplementedMethodError


