from molsysmt._private.digestion import digest

@digest()
def get_chain_id(molecular_system, element='atom', selection='all',
                 redefine_indices=False, redefined_ids=False,
                 syntax='MolSysMT', skip_digestion=False):

    if redefine_indices:

        raise NotImplementedError

    elif redefine_indices:

        raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_index=True, skip_digestion=True)

    return output

