def from_rdkit_Mol(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import Topology
    import numpy as np

    tmp_item = Topology()

    n_atoms = item.GetAtoms()

    atom_index_array = np.empty(n_atoms, dtype=int)
    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    atom_bonded_atom_indices_array = np.empty(n_atoms, dtype=object)

    #group_index_array = np.empty(n_atoms, dtype=int)
    #group_name_array = np.empty(n_atoms, dtype=object)
    #group_id_array = np.empty(n_atoms, dtype=int)
    #group_type_array = np.empty(n_atoms, dtype=object)

    #chain_index_array = np.empty(n_atoms, dtype=int)
    #chain_name_array = np.empty(n_atoms, dtype=object)
    #chain_id_array = np.empty(n_atoms, dtype=object)
    #chain_type_array = np.empty(n_atoms, dtype=object)

    rdkit_index_to_molsys_index={}
    atom_mapid={}

    atom_index = 0

    for atom in item.GetAtoms():

        atom_id = atom.GetIdx()
        try:
            map_id = int(atom.GetProp("_map_idx"))
        except KeyError:
            map_id = atom.GetAtomMapNum()

        atomic_number = atom.GetAtomicNum()
        if atom.HasProp("_Name"):
            atom_name = rda.GetProp("_Name")
        else:
            # check for PDB names
            try:
                atom_name = atom.GetMonomerInfo().GetName().strip()
            except AttributeError:
                atom_name = ""

        rdkit_index_to_molsys_index[rd_idx] = atom_index
        atom_mapid[atom_index] = map_id

        atom_index_array[atom_index] = atom_index
        atom_name_array[atom_index] = atom_name
        atom_id_array[atom_index] = atom_id
        atom_type_array[atom_index] = atomic_number

        atom_index += 1

    tmp_item.atoms_dataframe["atom_index"] = atom_index_array
    tmp_item.atoms_dataframe["atom_name"] = atom_name_array
    tmp_item.atoms_dataframe["atom_id"] = atom_id_array
    tmp_item.atoms_dataframe["atom_type"] = atom_type_array
    del(atom_index_array, atom_name_array, atom_id_array, atom_type_array)

    n_bonds = item.GetNumBonds()

    bond_atom1_array = empty(n_bonds, dtype=int)
    bond_atom2_array = empty(n_bonds, dtype=int)
    bond_type_array = empty(n_bonds, dtype=object)
    bond_order_array = empty(n_bonds, dtype=object)

    bond_index = 0

    for bond in item.getBonds():

        atom1_rdkit_index = bond.GetBeginAtomIdx()
        atom2_rdkit_index = bond.GetEndAtomIdx()
        bond_atom1_index = rdkit_index_to_molsys_index[atom1_rdkit_index]
        bond_atom2_index = rdkit_index_to_molsys_index[atom2_rdkit_index]

        bond_order = int(bond.GetBondTypeAsDouble())
        if bond.GetIsAromatic():
            bond_type = "Aromatic"
        else:
            bond_type = "Aliphatic"

        bond_atom1_array[bond_index] = bond_atom1_index
        bond_atom2_array[bond_index] = bond_atom2_index
        bond_order_array[bond_index] = bond_order
        bond_type_array[bond_index] = bond_type

        bond_index +=1

    tmp_item.bonds_dataframe["atom1_index"] = bond_atom1_array
    tmp_item.bonds_dataframe["atom2_index"] = bond_atom2_array
    tmp_item.bonds_dataframe["order"] = bond_order_array
    tmp_item.bonds_dataframe["type"] = bond_type_array

    ## components

    #tmp_item._build_components()

    ### molecules

    #tmp_item._build_molecules()

    ### entity

    #tmp_item._build_entities()

    ## nan to None

    tmp_item._nan_to_None()

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

