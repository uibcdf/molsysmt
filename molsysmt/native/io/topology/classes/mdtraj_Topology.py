def to_mdtraj_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from mdtraj import Topology
    from mdtraj.core import element

    n_atoms = item.shape[0]

    atom_index_array = item["atom.index"].to_numpy()
    atom_name_array = item["atom.name"].to_numpy()
    atom_id_array = item["atom.id"].to_numpy()
    atom_type_array = item["atom.type"].to_numpy()
    atom_formal_charge_array = item["atom.formal_charge"].to_numpy()

    group_index_array = item["group.index"].to_numpy()
    group_name_array = item["group.name"].to_numpy()
    group_id_array = item["group.id"].to_numpy()
    group_type_array = item["group.type"].to_numpy()

    chain_index_array = item["chain.index"].to_numpy()
    chain_name_array = item["chain.name"].to_numpy()
    chain_id_array = item["chain.id"].to_numpy()
    chain_type_array = item["chain.type"].to_numpy()

    atom_bonded_atom_indices_array = item["atom.bonded_atom_indices"].to_numpy()

    tmp_item = Topology()

    former_group_index = -1
    former_chain_index = -1

    list_new_atoms = []

    for ii in range(n_atoms):

        atom_index = atom_index_array[ii]
        atom_name = atom_name_array[ii]
        atom_id = atom_id_array[ii]
        atom_type = atom_type_array[ii]

        group_index = group_index_array[ii]
        chain_index = chain_index_array[ii]

        new_group = (former_group_index!=group_index)
        new_chain = (former_chain_index!=chain_index)

        if new_chain:
            chain = tmp_item.add_chain()
            former_chain_index = chain_index

        if new_group:
            residue_name = group_name_array[ii]
            residue_id = group_id_array[ii]
            residue = tmp_item.add_residue(residue_name, chain, resSeq=str(residue_id))
            former_group_index = group_index

        elem = element.get_by_symbol(atom_type)
        atom = tmp_item.add_atom(atom_name, elem, residue)

        list_new_atoms.append(atom)

    for ii, bonded_atom_indices in zip(atom_index_array, atom_bonded_atom_indices_array):

        atom_0 = list_new_atoms[ii]
        for jj in bonded_atom_indices:
            if ii < jj:
                atom_1 = list_new_atoms[jj]
                tmp_item.add_bond(atom_0, atom_1) # falta bond type and bond order

    return tmp_item

def from_mdtraj_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import Topology
    from numpy import empty, array, arange, reshape, where, unique, nan, sort
    from molsysmt.elements.group import name_to_type as group_name_to_group_type
    from networkx import empty_graph, connected_components

    tmp_item = Topology()

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

    molecule_index_array = empty(n_atoms, dtype=int)
    molecule_index_array.fill(0)
    tmp_item["molecule.index"] = molecule_index_array

    del(molecule_index_array)

    entity_index_array = empty(n_atoms, dtype=int)
    entity_index_array.fill(0)
    tmp_item["entity.index"] = entity_index_array

    del(entity_index_array)

    return tmp_item

