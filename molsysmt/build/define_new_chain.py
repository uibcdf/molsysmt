from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def define_new_chain(molecular_system, selection='all', chain_id=None, chain_name=None, syntax='MolSysMT',
                     skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get, set, select, get_form
    from molsysmt.element.chain import all_chain_names
    from molsysmt._private.atom_indices import complementary_atom_indices

    if is_all(selection):

        if chain_id is None:
            chain_id = 0
        if chain_name is None:
            chain_name = 'A'

        set(molecular_system, element='atom', selection='all', chain_index=0, skip_digestion=True)
        set(molecular_system, element='chain', selection='all', chain_id=[chain_id], chain_name=[chain_name], skip_digestion=True)

    else:

        atom_indices = select(molecular_system, selection=selection)
        rest_atom_indices = complementary_atom_indices(molecular_system, atom_indices)

        former_chain_ids, former_chain_names = get(molecular_system, selection=rest_atom_indices, chain_id=True,
                                                   chain_name=True)


        aux_chain_ids = sorted(np.unique(former_chain_ids).tolist())
        aux_chain_names = sorted(np.unique(former_chain_names).tolist())

        if chain_id is None:
            for ii in range(len(aux_chain_ids)):
                if ii not in aux_chain_ids:
                    chain_id = ii
                    break
            if chain_id is None:
                chain_id = len(aux_chain_ids)
        else:
            if chain_id in aux_chain_ids:
                raise ValueError(f'There is already a chain with chain_id={chain_id}.')

        if chain_name is None:
            for ii in all_chain_names:
                if ii not in aux_chain_names:
                    chain_name = ii
                    break
            if chain_name is None:
                raise ValueError(f'MolSysMT run out of chain names')
        else:
            if chain_name in aux_chain_names:
                raise ValueError(f'There is already a chain with chain_name={chain_name}.')


        all_atom_indices = np.array(atom_indices+rest_atom_indices)
        all_chain_ids = np.array([chain_id for ii in atom_indices]+former_chain_ids)
        all_chain_names = np.array([chain_name for ii in atom_indices]+former_chain_names)
        sorted_indices = np.argsort(all_atom_indices)
        all_atom_indices = all_atom_indices[sorted_indices]
        all_chain_ids = all_chain_ids[sorted_indices]
        all_chain_names = all_chain_names[sorted_indices]

        chain_index=-1
        chain_ids_done=[]
        new_chain_indices=[]
        new_chain_ids=[]
        new_chain_names=[]
        aux_dict={}
        for ii,jj,kk in zip(all_atom_indices, all_chain_ids, all_chain_names):
            if jj not in chain_ids_done:
                chain_index+=1
                aux_dict[jj]=chain_index
                chain_ids_done.append(jj)
                new_chain_indices.append(chain_index)
                new_chain_ids.append(jj)
                new_chain_names.append(kk)
            else:
                new_chain_indices.append(aux_dict[jj])

        n_chains=chain_index+1

        form_in = get_form(molecular_system)
        if form_in=='molsysmt.MolSys':
            molecular_system.topology.reset_chains(n_chains=n_chains)
        elif form_in=='molsysmt.Topology':
            molecular_system.reset_chains(n_chains=n_chains)

        set(molecular_system, element='atom', selection='all', chain_index=new_chain_indices, skip_digestion=True)
        set(molecular_system, element='chain', selection='all', chain_id=new_chain_ids, chain_name=new_chain_names,
            skip_digestion=True)

        if form_in=='molsysmt.MolSys':
            molecular_system.topology.rebuild_chains(redefine_ids=False, redefine_types=True, redefine_names=False)
        elif form_in=='molsysmt.Topology':
            molecular_system.rebuild_chains(redefine_ids=False, redefine_types=True, redefine_names=False)

        del new_chain_indices, new_chain_ids, new_chain_names
        del all_atom_indices, all_chain_ids, all_chain_names
        del atom_indices, rest_atom_indices

    pass

