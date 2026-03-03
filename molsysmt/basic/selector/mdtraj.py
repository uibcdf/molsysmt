from molsysmt._private.smonitor import NotImplementedMethodError

def select(molecular_system, selection='all', structure_indices='all'):

    from molsysmt.basic import convert, get_form

    form_in = get_form(molecular_system)

    if form_in == 'mdtraj.Topology':
        tmp_item = molecular_system
    else:
        tmp_item = convert(molecular_system, to_form='mdtraj.Topology')

    atom_indices = tmp_item.select(selection)

    return atom_indices


def indices_to_selection(molecular_system, indices, element='atom'):

    output_string = ''

    if element=='atom':
        output_string = 'index '+' '.join([str(ii) for ii in indices])
    elif element=='group':
        output_string = 'resid '+' '.join([str(ii) for ii in indices])
    elif element=='chain':
        output_string = 'chainid '+' '.join([str(ii) for ii in indices])
    else:
        raise NotImplementedMethodError(caller='molsysmt.basic.selector.mdtraj.indices_to_selection')

    return output_string

