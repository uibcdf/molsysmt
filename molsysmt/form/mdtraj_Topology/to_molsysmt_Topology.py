from molsysmt._private.digestion import digest
from molsysmt.element.group import get_group_type_from_group_name
import numpy as np

@digest(form='mdtraj.Topology')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    #from ..openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    #tmp_item = item.to_openmm()
    #tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    from molsysmt.native import Topology
    from ..molsysmt_Topology import extract


    n_atoms = item.n_atoms
    n_groups = item.n_residues
    n_chains = item.n_chains
    n_bonds = item.n_bonds

    tmp_item = Topology(n_atoms=n_atoms, n_groups=n_groups, n_chains=n_chains, n_bonds=n_bonds)

    # atoms

    for atom_index, atom in enumerate(item.atoms):

        if atom.serial is not None:
            tmp_item.atoms.iat[atom_index,0] = atoms.serial
        else:
            tmp_item.atoms.iat[atom_index,0] = atom_index
        tmp_item.atoms.iat[atom_index,1] = atom.name
        tmp_item.atoms.iat[atom_index,2] = atom.element.symbol
        tmp_item.atoms.iat[atom_index,3] = atom.residue.index
        tmp_item.atoms.iat[atom_index,4] = atom.residue.chain.index


    # groups

    aux_dict = {}

    for group_index, residue in enumerate(item.residues):

        tmp_item.groups.iat[group_index,1] = residue.name
        tmp_item.groups.iat[group_index,0] = residue.resSeq

        if residue.name not in aux_dict:
            aux_dict[residue.name] = get_group_type_from_group_name(residue.name)
        
        tmp_item.groups.iat[group_index,2] = aux_dict[residue.name]


    # chains

    for chain_index, chain in enumerate(item.chains):

        tmp_item.chains.iat[chain_index,0] = chain_index
        tmp_item.chains.iat[chain_index,1] = chain.chain_id

    rebuild_chain_name = tmp_item.chains['chain_name'].isna().all()

    # bonds

    for bond_index, bond in enumerate(item.bonds):

        tmp_item.bonds.iat[bond_index,0] = bond.atom1.index
        tmp_item.bonds.iat[bond_index,1] = bond.atom2.index
        tmp_item.bonds.iat[bond_index,2] = bond.order
        tmp_item.bonds.iat[bond_index,3] = bond.type

    if tmp_item.bonds["order"].isnull().all():
        tmp_item.bonds.drop("order", axis=1, inplace=True)

    if tmp_item.bonds["type"].isnull().all():
        tmp_item.bonds.drop("type", axis=1, inplace=True)

    tmp_item.bonds._sort_bonds()

    # components

    tmp_item.rebuild_components(redefine_indices=True, redefine_ids=True, redefine_names=True,
                                redefine_types=True)

    # molecules

    tmp_item.rebuild_molecules(redefine_indices=True, redefine_ids=True, redefine_names=True,
                               redefine_types=True)

    # chains
    tmp_item.rebuild_chains(redefine_ids=True, redefine_types=True, redefine_names=rebuild_chain_name)

    # entity

    tmp_item.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True,
                               redefine_types=True)

    tmp_item = tmp_item.extract(atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)


    return tmp_item

