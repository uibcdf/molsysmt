from molsysmt._private.smonitor import NotImplementedMethodError

def select(molecular_system, selection='all', structure_indices='all'):

    #from . import convert, get_form

    #if form_in == 'pytraj.Topology':
    #    tmp_item = item
    #else:
    #    tmp_item = convert(item, to_form='pytraj.Topology')

    raise NotImplementedMethodError(caller='molsysmt.basic.selector.amber.select')

def indices_to_selection(molecular_system, indices, element='atom'):

    raise NotImplementedMethodError(caller='molsysmt.basic.selector.amber.indices_to_selection')

