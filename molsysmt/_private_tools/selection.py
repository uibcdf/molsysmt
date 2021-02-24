from .exceptions import BadCallError

syntaxis = [
    'MolSysMT',
    'Amber',
    'MDAnalysis',
    'MDTraj',
    'ParmEd',
    'NGLView',
]

syntaxis_from_lower = { ii.lower():ii for ii in syntaxis }

def digest_syntaxis(syntaxis):

    try:
        syntaxis = syntaxis_from_lower[syntaxis.lower()]
        return syntaxis
    except:
        raise BadCallError()

def digest_to_syntaxis(to_syntaxis):

    if to_syntaxis is None:
        return None
    else:
        return digest_syntaxis(to_syntaxis)

def digest_selection(selection, syntaxis="MolSysMT"):

    syntaxis = digest_syntaxis(syntaxis)

    if syntaxis=='MolSysMT':

        selection=selection.replace('backbone', '(atom_name==["CA", "N", "C", "O"])')

    return selection

def indices_to_selection(item, indices, target='atom', syntaxis=None):

    from molsysmt._private_tools.targets import digest_target

    syntaxis = digest_syntaxis(syntaxis)
    target = digest_target(target)

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

def selection_is_all(selection):

    output = False
    if type(selection) is str:
        if selection.lower()=='all':
            output = True

    return output

