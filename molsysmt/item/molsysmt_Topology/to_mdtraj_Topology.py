from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_mdtraj_Topology(item, atom_indices='all'):

    try:
        from mdtraj import Topology
        from mdtraj.core import element
    except:
        raise LibraryNotFound('mdtraj')

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

