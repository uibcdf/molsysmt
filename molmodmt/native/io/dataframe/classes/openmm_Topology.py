
def from_openmm_Topology(item, atom_indices='all', frame_indices='all'):


    from molmodmt.native import DataFrame
    from numpy import empty, array, arange, reshape, where, unique, nan, sort
    from molmodmt.elements.group import name_to_type as group_name_to_group_type
    from networkx import empty_graph, connected_components

    tmp_item = DataFrame()

    n_atoms = item.getNumAtoms()

    atom_index_array = empty(n_atoms, dtype=int)
    atom_name_array = empty(n_atoms, dtype=object)
    atom_id_array = empty(n_atoms, dtype=int)
    atom_type_array = empty(n_atoms, dtype=object)
    atom_bonded_atom_indices_array = empty(n_atoms, dtype=object)

    group_index_array = empty(n_atoms, dtype=int)
    group_name_array = empty(n_atoms, dtype=object)
    group_id_array = empty(n_atoms, dtype=int)
    group_type_array = empty(n_atoms, dtype=object)

    chain_index_array = empty(n_atoms, dtype=int)
    #chain_name_array = empty(n_atoms, dtype=object)
    chain_id_array = empty(n_atoms, dtype=object)
    #chain_type_array = empty(n_atoms, dtype=object)

    atom_index = 0

    for atom in item.atoms():

        atom_index_array[atom_index] = atom.index
        atom_name_array[atom_index] = atom.name
        atom_id_array[atom_index] = atom.id
        atom_type_array[atom_index] = atom.element.symbol

        group_index_array[atom_index] = atom.residue.index
        group_name_array[atom_index] = atom.residue.name
        group_id_array[atom_index] = atom.residue.id
        group_type_array[atom_index] = group_name_to_group_type(atom.residue.name)

        chain_index_array[atom_index] = atom.residue.chain.index
        chain_id_array[atom_index] = atom.residue.chain.id

        atom_index+=1

    tmp_item["atom.index"] = atom_index_array
    tmp_item["atom.name"] = atom_name_array
    tmp_item["atom.id"] = atom_id_array
    tmp_item["atom.type"] = atom_type_array
    del(atom_index_array, atom_name_array, atom_id_array, atom_type_array)

    tmp_item["group.index"] = group_index_array
    tmp_item["group.name"] = group_name_array
    tmp_item["group.id"] = group_id_array
    tmp_item["group.type"] = group_type_array
    del(group_index_array, group_name_array, group_id_array, group_type_array)

    tmp_item["chain.index"] = chain_index_array
    tmp_item["chain.id"] = chain_id_array
    del(chain_index_array, chain_id_array)

    G = empty_graph(n_atoms)

    for bond in item.bonds():
        G.add_edge(bond.atom1.index, bond.atom2.index)

    for atom_index in range(n_atoms):
        aux_list = list(G.neighbors(atom_index))
        if len(aux_list)>1:
            aux_list = list(sort(aux_list))
        atom_bonded_atom_indices_array[atom_index] = aux_list

    tmp_item["atom.bonded_atom_indices"] = atom_bonded_atom_indices_array
    del(atom_bonded_atom_indices_array)

    atom_indices_per_component = list(connected_components(G))
    del(G)

    component_index_array = empty(n_atoms, dtype=int)
    #component_name_array = empty(n_atoms, dtype=object)
    #component_id_array = empty(n_atoms, dtype=int)
    #component_type_array = empty(n_atoms, dtype=object)

    component_index = 0

    for atom_indices_of_component in atom_indices_per_component:
        for atom_index in atom_indices_of_component:

            component_index_array[atom_index] = component_index

        component_index += 1

    tmp_item["component.index"] = component_index_array

    del(component_index_array)

    bioassembly_index_array = empty(n_atoms, dtype=int)
    bioassembly_index_array.fill(0)
    tmp_item["bioassembly.index"] = bioassembly_index_array
    del(bioassembly_index_array)

    molecule_index_array = empty(n_atoms, dtype=int)
    molecule_index_array.fill(0)
    tmp_item["molecule.index"] = molecule_index_array
    del(molecule_index_array)

    entity_index_array = empty(n_atoms, dtype=int)
    entity_index_array.fill(0)
    tmp_item["entity.index"] = entity_index_array
    del(entity_index_array)

    return tmp_item

