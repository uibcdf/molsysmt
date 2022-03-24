from .exceptions import BadCallError

def indices_to_selection(molecular_system, indices, target='atom', syntaxis=None):

    from molsysmt._private.target import digest_target
    from molsysmt._private.molecular_system import digest_molecular_system

    syntaxis = digest_syntaxis(syntaxis)
    target = digest_target(target)
    molecular_system = digest_molecular_system(molecular_system)

    output_string = ''

    if syntaxis=='NGLView':

        if target=='atom':
            output_string = '@'+','.join([str(ii) for ii in indices])
        elif target=='group':
            from molsysmt import get
            group_ids, chain_ids = get(molecular_system, target='group', indices=indices, group_id=True, chain_id=True)
            output_string = ' '.join([str(ii)+':'+str(jj) for ii,jj in zip(group_ids, chain_ids)])
        elif target=='chain':
            from molsysmt import get
            chain_ids = get(molecular_system, target='chain', indices=indices, chain_id=True)
            output_string = ' '.join([':'+ii for ii in chain_ids])
        else:
            raise NotImplementedError

    elif syntaxis=='MDTraj':

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
        trimmed = selection.replace(' ','')
        if trimmed.lower()=='all':
            output = True

    return output


