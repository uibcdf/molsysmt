from molsysmt._private.digestion import digest

@digest()
def elements_to_string(molecular_system, indices=None, element='atom'):

    from molsysmt.basic import get

    element = digest_element(element)

    string=[]

    if element=='atom':

        atom_indices, atom_ids, atom_names = get(molecular_system, element=element, indices=indices, index=True,
                                                 id=True, name=True)
        for atom_index, atom_id, atom_name in zip(atom_indices, atom_ids, atom_names):
            string.append(atom_name+'-'+str(atom_id)+'@'+str(atom_index))

    elif element=='group':

        group_indices, group_ids, group_names = get(molecular_system, element=element, indices=indices, index=True,
                                                    id=True, name=True)
        for group_index, group_id, group_name in zip(group_indices, group_ids, group_names):
            string.append(group_name+'-'+str(group_id)+'@'+str(group_index))

    elif element=='component':

        component_indices = get(molecular_system, element=element, indices=indices, index=True)
        for component_index in component_indices:
            string.append(str(component_index))

    elif element=='chain':

        chain_indices, chain_ids, chain_names = get(molecular_system, element=element, indices=indices, index=True,
                                                    id=True, name=True)
        for chain_index, chain_id, chain_name in zip(chain_indices, chain_ids, chain_names):
            if chain_name is None:
                chain_name = '_'
            string.append(chain_name+'-'+str(chain_id)+'@'+str(chain_index))

    elif element=='molecule':

        molecule_indices, molecule_names = get(molecular_system, element=element, indices=indices, index=True,
                                               name=True)
        for molecule_index, molecule_name in zip(molecule_indices, molecule_names):
            if molecule_name is None:
                molecule_name = '_'
            string.append(molecule_name+'@'+str(molecule_index))

    elif element=='entity':

        entity_indices, entity_names = get(molecular_system, element=element, indices=indices, index=True, name=True)
        for entity_index, entity_name in zip(entity_indices, entity_names):
            if entity_name is None:
                molecule_name = '_'
            string.append(entity_name+'@'+str(entity_index))

    return string

