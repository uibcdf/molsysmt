
def from_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native import DataFrame
    from molsysmt.forms.classes.api_molsysmt_DataFrame import extract_subsystem
    from numpy import empty, array, arange, reshape, where, unique, nan, sort
    from molsysmt.elements.group import name_to_type as group_name_to_group_type
    from networkx import empty_graph, connected_components

    tmp_item = DataFrame()

    n_atoms = item.n_atoms

    mdtraj_dataframe, mdtraj_bonds = item.to_dataframe()

    tmp_item["atom.index"] = list(mdtraj_dataframe.index)
    tmp_item["atom.id"] = mdtraj_dataframe["serial"]
    tmp_item["atom.name"] = mdtraj_dataframe["name"]
    tmp_item["atom.type"] = mdtraj_dataframe["element"]

    tmp_item["group.id"] = mdtraj_dataframe["resSeq"]
    tmp_item["group.name"] = mdtraj_dataframe["resName"]

    tmp_item["chain.id"] = mdtraj_dataframe["chainID"]

    del(mdtraj_dataframe)

    group_type_array = empty(n_atoms, dtype=object)

    tmp_item["group.type"] = list(map(group_name_to_group_type,tmp_item["group.name"]))

    G = empty_graph(n_atoms)

    atom_bonded_atom_indices_array = empty(n_atoms, dtype=object)

    for mdtraj_bond in mdtraj_bonds:
        G.add_edge(int(mdtraj_bond[0]), int(mdtraj_bond[1]))

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

    group_index_array = empty(n_atoms, dtype=int)
    chain_index_array = empty(n_atoms, dtype=int)

    for atom in item.atoms:
        atom_index = atom.index
        group_index_array[atom_index] = atom.residue.index
        chain_index_array[atom_index] = atom.residue.chain.index

    tmp_item["group.index"] = group_index_array
    tmp_item["chain.index"] = chain_index_array

    del(group_index_array, chain_index_array)

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

