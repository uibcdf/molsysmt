def to_pytraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from pytraj import Topology
    from pytraj import Atom as pytraj_atom, Residue as pytraj_residue
    from molsysmt.physico_chemical_properties import mass as get_mass
    from molsysmt.physico_chemical_properties import charge as get_charge
    from molsysmt import puw

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

    mass_atom_array = puw.get_value(get_mass(item))
    try:
        charge_atom_array = get_charge(molecular_system)
    except:
        charge_atom_array = np.zeros(shape=[n_atoms])

    tmp_item = Topology()

    former_group_index = -1

    list_new_atoms = []

    for ii in range(n_atoms):

        atom_index = atom_index_array[ii]
        atom_name = atom_name_array[ii]
        atom_id = atom_id_array[ii]
        atom_type = atom_type_array[ii]
        atom_charge = atom_charge_array[ii]
        atom_mass = atom_mass_array[ii]

        group_index = group_index_array[ii]
        chain_index = chain_index_array[ii]

        new_group = (former_group_index!=group_index)

        if new_group:
            residue_name = group_name_array[ii]
            residue_id = group_id_array[ii]
            residue = pytraj_residue(residue_name, resid=group_index, icode=residue_id, chainID=chain_index)
            former_group_index = group_index

        atom = pytraj_atom(name=atom_name, type=atom_type, resid=group_index, mass=atom_mass, charge=atom_charge)

        list_new_atoms.append(atom)

        tmp_item.add_atom(atom, residue)

    bonds = np.column_stack(bonds_atom1, bonds_atom2)
    tmp_item.add_bonds(bonds)

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item


def from_pytraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

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

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

