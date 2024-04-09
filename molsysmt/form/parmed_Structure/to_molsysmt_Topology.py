from molsysmt._private.digestion import digest
import numpy as np
from molsysmt.element.group import get_group_type_from_group_name
from molsysmt.element.atom import get_atom_type_from_atom_name

@digest(form='parmed.Structure')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from ..molsysmt_Topology import extract

    tmp_item = Topology()

    n_atoms = len(item.atoms)
    n_groups = len(item.residues)
    n_bonds = len(item.bonds)

    tmp_item.reset_atoms(n_atoms=n_atoms)
    tmp_item.reset_groups(n_groups=n_groups)
    tmp_item.reset_bonds(n_bonds=n_bonds)

    atom_index = 0
    former_group_index = -1
    former_chain_index = -1

    aux_dict_chains={}

    for atom in item.atoms:

        group_index = atom.residue.idx

        chain_id = atom.residue.chain
        if chain_id not in aux_dict_chains:
            aux_dict_chains[chain_id]=len(aux_dict_chains)
        chain_index = aux_dict_chains[chain_id]


        tmp_item.atoms.iloc[atom_index,0] = atom.idx
        tmp_item.atoms.iloc[atom_index,1] = atom.name
        tmp_item.atoms.iloc[atom_index,2] = get_atom_type_from_atom_name(atom.name)
        tmp_item.atoms.iloc[atom_index,3] = group_index
        tmp_item.atoms.iloc[atom_index,4] = chain_index

        if former_group_index!=group_index:
            tmp_item.groups.iloc[group_index,0] = atom.residue.idx
            tmp_item.groups.iloc[group_index,1] = atom.residue.name
            tmp_item.groups.iloc[group_index,2] = get_group_type_from_group_name(atom.residue.name)
            former_group_index+=1

        atom_index+=1

    n_chains=len(aux_dict_chains)

    tmp_item.reset_chains(n_chains=n_chains)

    if len(aux_dict_chains)==1:
        if '' in aux_dict_chains:
            aux_dict_chains['A']=aux_dict_chains['']
            del aux_dict_chains['']

    for chain_id, chain_index in aux_dict_chains.items():
        tmp_item.chains.iloc[chain_index,0] = chain_index
        tmp_item.chains.iloc[chain_index,1] = chain_id

    # bonds

    bond_index = 0

    for bond in item.bonds:

        tmp_item.bonds.iloc[bond_index,0] = bond.atom1._idx
        tmp_item.bonds.iloc[bond_index,1] = bond.atom2._idx

        bond_index +=1

    # components

    tmp_item.rebuild_components()

    ## molecules

    tmp_item.rebuild_molecules()

    ## entity

    tmp_item.rebuild_entities()

    ## extract if atom_indices is not 'all'

    tmp_item = extract(tmp_item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

