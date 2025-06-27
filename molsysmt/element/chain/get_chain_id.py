from molsysmt._private.digestion import digest

@digest()
def get_chain_id(molecular_system, element='atom', selection='all',
                 redefine_indices=False, redefine_ids=False,
                 syntax='MolSysMT', skip_digestion=False):

    if redefine_ids:

        from .get_chain_index import get_chain_index

        output = get_chain_index(molecular_system, element=element, selection=selection, syntax=syntax,
                                 redefine_indices=redefine_indices, skip_digestion=True)

        

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_index=True, skip_digestion=True)

    return output

