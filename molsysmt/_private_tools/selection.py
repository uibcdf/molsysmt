from .exceptions import BadCallError

list_syntaxis = [
    'MolSysMT',
    'Amber',
    'MDAnalysis',
    'MDTraj',
    'ParmEd',
    'NGLView',
]

_aux={ ii.lower():ii for ii in list_syntaxis }

def digest_syntaxis(syntaxis):

    try:
        syntaxis = _aux[syntaxis.lower()]
        return syntaxis
    except:
        raise BadCallError('Wrong way of invoking this method. Either the engine is not implemented, either is mispelled.\n\
                           Check the online documentation  for more information: http://www.uibcdf.org/MolSysMT')


def digest_to_syntaxis(to_syntaxis):

    if to_syntaxis is None:
        return None
    else:
        return digest_syntaxis(to_syntaxis)

def digest_selection(selection, syntaxis="MolSysMT"):

    syntaxis = digest_syntaxis(syntaxis)

    if syntaxis=='MolSysMT':

        selection=selection.replace('backbone', '(atom_name==["CA", "N", "C", "O"])')

    return selection, syntaxis

def indices_to_selection(item, indices, target='atom', syntaxis=None):

    syntaxis = digest_syntaxis(syntaxis)

    output_string = ''

    if syntaxis=='NGLview':

        if target=='atom':
            output_string = '@'+','.join([str(ii) for ii in indices])
        elif target=='group':
            from molsysmt import get
            group_ids, chain_ids = get(item, target='group', indices=indices, group_id=True, chain_id=True)
            output_string = ' '.join([str(ii)+':'+str(jj) for ii,jj in zip(group_ids, chain_ids)])
        elif target=='chain':
            from molsysmt import get
            chain_ids = get(item, target='chain', indices=indices, chain_id=True)
            output_string = ' '.join([':'+ii for ii in chain_ids])
        else:
            raise NotImplementedError

    elif to_syntaxis=='MDTraj':

        if target=='atom':
            output_string = 'index '+' '.join([str(ii) for ii in indices])
        elif target=='group':
            output_string = 'resid '+' '.join([str(ii) for ii in indices])
        elif target=='chain':
            output_string = 'chainid '+' '.join([str(ii) for ii in indices])
        else:
            raise NotImplementedError

    else:

        raise NotImplementedError

    return output_string

