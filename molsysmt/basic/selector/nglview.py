import numpy as np
from molsysmt._private.exceptions import NotImplementedMethodError

def select(molecular_system, selection='all', structure_indices='all'):

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
        group_ids, chain_names = get(molecular_system, element='group', selection=indices, group_id=True, chain_name=True)
        if np.all(np.isin(np.unique(chain_names), [' ', None])):
            output_string = ','.join([str(ii) for ii in group_ids])
        else:
            output_string = ' '.join([str(ii)+':'+str(jj) for ii,jj in zip(group_ids, chain_names)])
    elif element=='chain':
        from molsysmt import get
        chain_names = get(molecular_system, element='chain', selection=indices, chain_id=True)
        output_string = ' '.join([':'+ii for ii in chain_names])
    else:
        raise NotImplementedMethodError

    return output_string

