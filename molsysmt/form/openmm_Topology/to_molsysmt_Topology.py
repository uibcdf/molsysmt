from molsysmt._private.arg_digestion import arg_digest
from molsysmt.element.group import get_group_type_from_group_name
import numpy as np

@arg_digest(form='openmm.Topology')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt.form.molsysmt_Topology.extract import extract as extract_molsysmt_Topology
    from molsysmt._private.variables import is_all

    n_atoms = item.getNumAtoms()
    n_groups = item.getNumResidues()
    n_chains = item.getNumChains()
    n_bonds = item.getNumBonds()

    tmp_item = Topology(n_atoms=n_atoms, n_groups=n_groups, n_chains=n_chains)

    # Atoms and Groups
    atom_id = []
    atom_name = []
    atom_type = []
    group_index_of_atoms = []
    
    group_id = []
    group_name = []
    group_type = []
    chain_index_of_groups = []

    for atom in item.atoms():
        atom_id.append(str(atom.id))
        atom_name.append(atom.name)
        atom_type.append(atom.element.symbol if atom.element else None)
        group_index_of_atoms.append(atom.residue.index)

    for residue in item.residues():
        group_id.append(str(residue.id))
        group_name.append(residue.name)
        group_type.append(get_group_type_from_group_name(residue.name))
        chain_index_of_groups.append(residue.chain.index)

    tmp_item.atoms.atom_id = atom_id
    tmp_item.atoms.atom_name = atom_name
    tmp_item.atoms.atom_type = atom_type
    tmp_item.atoms.group_index = group_index_of_atoms

    tmp_item.groups.group_id = group_id
    tmp_item.groups.group_name = group_name
    tmp_item.groups.group_type = group_type
    tmp_item.groups.chain_index = chain_index_of_groups

    # Chains
    chain_id = []
    chain_name = []
    for chain in item.chains():
        chain_id.append(str(chain.id))
        chain_name.append(str(chain.id))

    tmp_item.chains.chain_id = chain_id
    tmp_item.chains.chain_name = chain_name

    # Bonds
    if n_bonds > 0:
        bonded_atoms = []
        for bond in item.bonds():
            bonded_atoms.append([bond.atom1.index, bond.atom2.index])
        tmp_item.add_bonds(bonded_atoms, skip_digestion=True)

    # Rebuild remaining hierarchy
    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        tmp_item = extract_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
