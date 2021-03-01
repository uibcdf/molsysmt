def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    import simtk.openmm as mm
    import simtk.openmm.app as app
    import simtk.unit as unit
    from numpy import unique

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
            chain_id = chain_id_array[ii]
            chain = tmp_item.addChain(id=str(chain_id))
            former_chain_index = chain_index

        if new_group:
            residue_name = group_name_array[ii]
            residue_id = group_id_array[ii]
            residue = tmp_item.addResidue(residue_name, chain, id=str(residue_id))
            former_group_index = group_index

        element = app.Element.getBySymbol(atom_type)
        atom = tmp_item.addAtom(atom_name, element, residue)

        list_new_atoms.append(atom)

    for atom_1, atom_2 in zip(bonds_atom1, bonds_atom2):

        tmp_item.addBond(list_new_atoms[atom_1], list_new_atoms[atom_2]) # falta bond type and bond order

    return tmp_item

def from_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import Topology
    from numpy import empty, array, arange, reshape, where, unique, nan, sort, zeros
    from molsysmt.elements.group import name_to_type as group_name_to_group_type

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

    n_bonds = item.getNumBonds()

    bond_atom1_array = empty(n_bonds, dtype=int)
    bond_atom2_array = empty(n_bonds, dtype=int)
    bond_type_array = empty(n_bonds, dtype=object)
    bond_order_array = empty(n_bonds, dtype=object)

    bond_index = 0

    for bond in item.bonds():

        bond_atom1_array[bond_index] = bond.atom1.index
        bond_atom2_array[bond_index] = bond.atom2.index
        bond_order_array[bond_index] = bond.order
        bond_type_array[bond_index] = bond.type

        bond_index +=1

    tmp_item.bonds_dataframe["atom1_index"] = bond_atom1_array
    tmp_item.bonds_dataframe["atom2_index"] = bond_atom2_array
    tmp_item.bonds_dataframe["order"] = bond_order_array
    tmp_item.bonds_dataframe["type"] = bond_type_array

    # components

    tmp_item._build_components()

    ## molecules

    tmp_item._build_molecules()

    ## entity

    tmp_item._build_entities()

    ## nan to None

    tmp_item._nan_to_None()

    return tmp_item

