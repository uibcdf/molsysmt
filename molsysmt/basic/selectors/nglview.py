from molsysmt._private.exceptions import NotImplementedMethodError

def select(item, selection):

    #from . import convert, get_form

    #if form_in == 'pytraj.Topology':
    #    tmp_item = item
    #else:
    #    tmp_item = convert(item, to_form='pytraj.Topology')

    raise NotImplementedMethodError

def indices_to_selection(molecular_system, indices, element='atom'):

    output_string = ''

    if element=='atom':
        output_string = '@'+','.join([str(ii) for ii in indices])
    elif element=='group':
        from molsysmt import get
        group_ids, chain_ids = get(molecular_system, element='group', selection=indices, group_id=True, chain_id=True)
        if np.all(np.isin(np.unique(chain_ids), [' ', None])):
            output_string = ','.join([str(ii) for ii in group_ids])
        else:
            output_string = ' '.join([str(ii)+':'+str(jj) for ii,jj in zip(group_ids, chain_ids)])
    elif element=='chain':
        from molsysmt import get
        chain_ids = get(molecular_system, element='chain', selection=indices, chain_id=True)
        output_string = ' '.join([':'+ii for ii in chain_ids])
    else:
        raise NotImplementedMethodError

    return output_string

