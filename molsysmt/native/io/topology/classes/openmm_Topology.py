def to_openmm_Topology(item, trajectory_item='all', atom_indices='all', frame_indices='all'):

    import simtk.openmm as mm
    import simtk.openmm.app as app
    import simtk.unit as unit
    from numpy import unique

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

    tmp_item = app.Topology()

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
            chain = tmp_item.addChain()
            former_chain_index = chain_index

        if new_group:
            residue_name = group_name_array[ii]
            residue_id = group_id_array[ii]
            residue = tmp_item.addResidue(residue_name, chain, id=str(residue_id))
            former_group_index = group_index

        element = app.Element.getBySymbol(atom_type)
        atom = tmp_item.addAtom(atom_name, element, residue)

        list_new_atoms.append(atom)

    for ii, bonded_atom_indices in zip(atom_index_array, atom_bonded_atom_indices_array):

        atom_0 = list_new_atoms[ii]
        for jj in bonded_atom_indices:
            if ii < jj:
                atom_1 = list_new_atoms[jj]
                tmp_item.addBond(atom_0, atom_1) # falta bond type and bond order

    return tmp_item

def from_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native import Topology
    from numpy import empty, array, arange, reshape, where, unique, nan, sort, zeros
    from molsysmt.elements.group import name_to_type as group_name_to_group_type
    from networkx import empty_graph, connected_components

    tmp_item = Topology()

    n_atoms = item.getNumAtoms()

    # atoms, groups and chains

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
    chain_name_array = empty(n_atoms, dtype=object)
    chain_id_array = empty(n_atoms, dtype=object)
    chain_type_array = empty(n_atoms, dtype=object)

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
    del(group_index_array, group_id_array, group_name_array, group_type_array)

    tmp_item["chain.index"] = chain_index_array
    tmp_item["chain.id"] = chain_id_array
    del(chain_index_array, chain_id_array, chain_name_array, chain_type_array)

    # components

    component_index_array = empty(n_atoms, dtype=int)

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

    component_index = 0

    for atom_indices_of_component in connected_components(G):
        aux_list = list(atom_indices_of_component)
        component_index_array[aux_list] = component_index
        component_index += 1

    tmp_item["component.index"] = component_index_array

    del(G)

    # molecule

    tmp_item["molecule.index"] = component_index_array

    del(component_index_array)

    # entity

    entity_index_array = zeros(n_atoms, dtype=int)
    tmp_item["entity.index"] = entity_index_array
    del(entity_index_array)

    # rebuild components, molecules and entities:

    tmp_item._rebuild_components_molecules_entities()

    # nan to None

    tmp_item._nan_to_None()

    return tmp_item

