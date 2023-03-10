from molsysmt._private.digestion import digest

@digest(form='mdtraj.Topology')
def to_molsysmt_Topology(item, atom_indices='all'):

    from molsysmt.native import Topology
    import numpy as np
    from molsysmt.element.group import get_group_type_from_group_name

    tmp_item = Topology()

    n_atoms = item.n_atoms
    n_bonds = item.n_bonds

    mdtraj_dataframe, mdtraj_bonds = item.to_dataframe()

    tmp_item.atoms_dataframe["atom_index"] = mdtraj_dataframe.index.to_numpy()
    tmp_item.atoms_dataframe["atom_id"] = mdtraj_dataframe["serial"].to_numpy()
    tmp_item.atoms_dataframe["atom_name"] = mdtraj_dataframe["name"].to_numpy()
    tmp_item.atoms_dataframe["atom_type"] = mdtraj_dataframe["element"].to_numpy()

    tmp_item.atoms_dataframe["group_id"] = mdtraj_dataframe["resSeq"].to_numpy()
    tmp_item.atoms_dataframe["group_name"] = mdtraj_dataframe["resName"].to_numpy()

    tmp_item.atoms_dataframe["chain_id"] = mdtraj_dataframe["chainID"].to_numpy()

    tmp_item.bonds_dataframe["atom1_index"] = np.array(mdtraj_bonds[:,0], dtype=int)
    tmp_item.bonds_dataframe["atom2_index"] = np.array(mdtraj_bonds[:,1], dtype=int)

    del(mdtraj_dataframe)

    group_type_array = np.empty(n_atoms, dtype=object)

    tmp_item.atoms_dataframe["group_type"] = [get_group_type_from_group_name(ii) for ii in tmp_item.atoms_dataframe["group_name"]]


    group_index_array = np.empty(n_atoms, dtype=int)
    chain_index_array = np.empty(n_atoms, dtype=int)

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

    ## nan to None

    tmp_item._nan_to_None()

    ##

    return tmp_item

