from molsysmt._private.digestion import digest

@digest(form='pytraj.Topology')
def to_molsysmt_Topology(item, atom_indices='all'):

    from molsysmt.native import Topology
    import numpy as np
    from molsysmt.elements.group import name_to_type as group_name_to_group_type
    from networkx import empty_graph, connected_components

    tmp_item = Topology()

    n_atoms = item.n_atoms

    # atoms, groups and chains

    atom_index_array = np.empty(n_atoms, dtype=int)
    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=object)
    atom_type_array = np.empty(n_atoms, dtype=object)
    atom_bonded_atom_indices_array = np.empty(n_atoms, dtype=object)

    group_index_array = np.empty(n_atoms, dtype=int)
    group_name_array = np.empty(n_atoms, dtype=object)
    group_id_array = np.empty(n_atoms, dtype=int)
    group_type_array = np.empty(n_atoms, dtype=object)

    chain_index_array = np.empty(n_atoms, dtype=int)
    chain_name_array = np.empty(n_atoms, dtype=object)
    chain_id_array = np.empty(n_atoms, dtype=object)
    chain_type_array = np.empty(n_atoms, dtype=object)

    atom_index = 0

    for atom in item.atoms:

        atom_index_array[atom_index] = atom.index
        atom_name_array[atom_index] = atom.name
        atom_id_array[atom_index] = None
        atom_type_array[atom_index] = atom.type

        group_index_array[atom_index] = atom.resid
        group_name_array[atom_index] = atom.resname
        group_id_array[atom_index] = item.residue(atom.resid).original_resid
        group_type_array[atom_index] = group_name_to_group_type(atom.resname)

        chain_index_array[atom_index] = atom.chain
        chain_id_array[atom_index] = None

        atom_index+=1

    tmp_item.atoms_dataframe["atom_index"] = atom_index_array
    tmp_item.atoms_dataframe["atom_name"] = atom_name_array
    tmp_item.atoms_dataframe["atom_id"] = atom_id_array
    tmp_item.atoms_dataframe["atom_type"] = atom_type_array
    del(atom_index_array, atom_name_array, atom_id_array, atom_type_array)

    tmp_item.atoms_dataframe["group_index"] = group_index_array
    tmp_item.atoms_dataframe["group_name"] = group_name_array
    tmp_item.atoms_dataframe["group_id"] = group_id_array
    tmp_item.atoms_dataframe["group_type"] = group_type_array
    del(group_index_array, group_id_array, group_name_array, group_type_array)

    tmp_item.atoms_dataframe["chain_index"] = chain_index_array
    tmp_item.atoms_dataframe["chain_id"] = chain_id_array
    del(chain_index_array, chain_id_array, chain_name_array, chain_type_array)

    # bonds

    try:
        n_bonds = item.bond_indices.shape[0]
    except:
        n_bonds = 0

    if n_bonds > 0:

        bond_atom1_array = item.bond_indices[:,0]
        bond_atom2_array = item.bond_indices[:,1]
        bond_type_array = np.full(n_bonds, None, dtype=object)
        bond_order_array = np.full(n_bonds, None, dtype=object)

        tmp_item.bonds_dataframe["atom1_index"] = bond_atom1_array
        tmp_item.bonds_dataframe["atom2_index"] = bond_atom2_array
        tmp_item.bonds_dataframe["order"] = bond_order_array
        tmp_item.bonds_dataframe["type"] = bond_type_array

        del(bond_atom1_array, bond_atom2_array, bond_type_array, bond_order_array)

    # components

    tmp_item._build_components()

    ## molecules

    tmp_item._build_molecules()

    ## entity

    tmp_item._build_entities()

    ## nan to None

    tmp_item._nan_to_None()

    return tmp_item

def _to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Topology(item, atom_indices=atom_indices)

