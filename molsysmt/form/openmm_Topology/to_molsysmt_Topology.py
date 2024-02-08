from molsysmt._private.digestion import digest
from molsysmt.element.group.get_group_type import _get_group_type_from_group_name
import numpy as np

@digest(form='openmm.Topology')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from ..molsysmt_Topology import extract

    tmp_item = Topology()

    n_atoms = item.getNumAtoms()
    n_groups = item.getNumResidues()
    n_chains = item.getNumChains()
    n_bonds = item.getNumBonds()

    # atoms

    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    group_index_array = np.empty(n_atoms, dtype=int)
    chain_index_array = np.empty(n_atoms, dtype=int)

    index = 0

    for atom in item.atoms():

        atom_name_array[index] = atom.name
        atom_id_array[index] = atom.id
        atom_type_array[index] = atom.element.symbol

        group_index_array[index] = atom.residue.index
        chain_index_array[index] = atom.residue.chain.index

        index += 1

    tmp_item.atoms["atom_name"] = atom_name_array
    tmp_item.atoms["atom_id"] = atom_id_array
    tmp_item.atoms["atom_type"] = atom_type_array
    tmp_item.atoms["group_index"] = group_index_array
    tmp_item.atoms["chain_index"] = chain_index_array

    del atom_name_array, atom_id_array, atom_type_array
    del group_index_array, chain_index_array

    # groups

    group_id_array = np.empty(n_groups, dtype=int)
    group_name_array = np.empty(n_groups, dtype=object)

    index = 0

    aux_dict = {}

    for residue in item.residues():

        group_id_array[index] = residue.id
        group_name_array[index] = residue.name

        if residue.name not in aux_dict:
            aux_dict[residue.name] = _get_group_type_from_group_name(residue.name)

        index += 1

    tmp_item.groups["group_id"] = group_id_array
    tmp_item.groups["group_name"] = group_name_array
    tmp_item.groups["group_type"] = np.array([aux_dict[ii] for ii in group_name_array], dtype=object)

    del group_id_array, group_name_array

    # chains

    chain_name_array = np.empty(n_chains, dtype=object)

    index = 0

    for chain in item.chains():

        chain_name_array[index] = chain.id

    tmp_item.chains["chain_name"] = chain_name_array
    tmp_item.chains["chain_id"] = tmp_item.chains.index

    del chain_name_array

    # bonds

    bond_atom1_array = np.empty(n_bonds, dtype=int)
    bond_atom2_array = np.empty(n_bonds, dtype=int)
    bond_type_array = np.empty(n_bonds, dtype=object)
    bond_order_array = np.empty(n_bonds, dtype=object)

    index = 0

    for bond in item.bonds():

        bond_atom1_array[index] = bond.atom1.index
        bond_atom2_array[index] = bond.atom2.index
        bond_order_array[index] = bond.order
        bond_type_array[index] = bond.type

        index += 1

    tmp_item.bonds["atom1_index"] = bond_atom1_array
    tmp_item.bonds["atom2_index"] = bond_atom2_array
    tmp_item.bonds["order"] = bond_order_array
    tmp_item.bonds["type"] = bond_type_array

    del bond_atom1_array, bond_atom2_array
    del bond_order_array, bond_type_array

    if tmp_item.bonds["order"].isnull().all():
        tmp_item.bonds.drop("order", axis=1, inplace=True)

    if tmp_item.bonds["type"].isnull().all():
        tmp_item.bonds.drop("type", axis=1, inplace=True)

    # components

    tmp_item.rebuild_components()

    # molecules

    tmp_item.rebuild_molecules()

    # chain types

    tmp_item.rebuild_chain_types()

    # entity

    tmp_item.rebuild_entities()

    # nan to None

    tmp_item._fix_null_values()
    tmp_item.bonds._sort_bonds()

    tmp_item = tmp_item.extract(atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item
