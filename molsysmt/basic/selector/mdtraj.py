from molsysmt._private.exceptions import NotImplementedMethodError

def select(item, selection):

    from . import convert, get_form

    form_in = get_form(item)

    if form_in == 'mdtraj.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='mdtraj.Topology')

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
        raise NotImplementedMethodError

    return output_string

