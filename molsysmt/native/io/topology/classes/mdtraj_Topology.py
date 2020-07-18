def to_mdtraj_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from mdtraj import Topology
    from mdtraj.core import element

    n_atoms = item.atoms_dataframe.shape[0]

    atom_index_array = item.atoms_dataframe["atom_index"].to_numpy()
    atom_name_array = item.atoms_dataframe["atom_name"].to_numpy()
    atom_id_array = item.atoms_dataframe["atom_id"].to_numpy()
    atom_type_array = item.atoms_dataframe["atom_type"].to_numpy()

    group_index_array = item.atoms_dataframe["group_index"].to_numpy()
    group_name_array = item.atoms_dataframe["group_name"].to_numpy()
    group_id_array = item.atoms_dataframe["group_id"].to_numpy()
    group_type_array = item.atoms_dataframe["group_type"].to_numpy()

    chain_index_array = item.atoms_dataframe["chain_index"].to_numpy()
    chain_name_array = item.atoms_dataframe["chain_name"].to_numpy()
    chain_id_array = item.atoms_dataframe["chain_id"].to_numpy()
    chain_type_array = item.atoms_dataframe["chain_type"].to_numpy()

    bonds_atom1 = item.bonds_dataframe["atom1_index"].to_numpy()
    bonds_atom2 = item.bonds_dataframe["atom2_index"].to_numpy()

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

    for atom_1, atom_2 in zip(bonds_atom1, bonds_atom2):

        tmp_item.add_bond(list_new_atoms[atom_1], list_new_atoms[atom_2]) # falta bond type and bond order

    return tmp_item

def from_mdtraj_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import Topology
    from numpy import empty, array, arange, reshape, where, unique, nan, sort
    from molsysmt.elements.group import name_to_type as group_name_to_group_type

    tmp_item = Topology()

    n_atoms = item.n_atoms
    n_bonds = item.n_bonds

    mdtraj_dataframe, mdtraj_bonds = item.to_dataframe()

    tmp_item.atoms_dataframe["atom_index"] = list(mdtraj_dataframe.index)
    tmp_item.atoms_dataframe["atom_id"] = mdtraj_dataframe["serial"]
    tmp_item.atoms_dataframe["atom_name"] = mdtraj_dataframe["name"]
    tmp_item.atoms_dataframe["atom_type"] = mdtraj_dataframe["element"]

    tmp_item.atoms_dataframe["group_id"] = mdtraj_dataframe["resSeq"]
    tmp_item.atoms_dataframe["group_name"] = mdtraj_dataframe["resName"]

    tmp_item.atoms_dataframe["chain_id"] = mdtraj_dataframe["chainID"]

    tmp_item.bonds_dataframe["atom1_index"] = array(mdtraj_bonds[:,0], dtype=int)
    tmp_item.bonds_dataframe["atom2_index"] = array(mdtraj_bonds[:,1], dtype=int)

    del(mdtraj_dataframe)

    group_type_array = empty(n_atoms, dtype=object)

    tmp_item.atoms_dataframe["group_type"] = list(map(group_name_to_group_type,tmp_item.atoms_dataframe["group_name"]))


    group_index_array = empty(n_atoms, dtype=int)
    chain_index_array = empty(n_atoms, dtype=int)

    for atom in item.atoms:
        atom_index = atom.index
        group_index_array[atom_index] = atom.residue.index
        chain_index_array[atom_index] = atom.residue.chain.index

    tmp_item.atoms_dataframe["group_index"] = group_index_array
    tmp_item.atoms_dataframe["chain_index"] = chain_index_array

    del(group_index_array, chain_index_array)

    tmp_item._build_components()
    tmp_item._build_molecules()
    tmp_item._build_entities()

    return tmp_item

