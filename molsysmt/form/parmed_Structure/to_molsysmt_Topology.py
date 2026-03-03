from molsysmt._private.arg_digestion import arg_digest
from molsysmt.element.group import get_group_type_from_group_name
from molsysmt.element.atom import get_atom_type_from_atom_name
import numpy as np

@arg_digest(form='parmed.Structure')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt.form.molsysmt_Topology.extract import extract as extract_molsysmt_Topology
    from molsysmt._private.variables import is_all

    n_atoms = len(item.atoms)
    n_groups = len(item.residues)
    n_bonds = len(item.bonds)

    # ParmEd doesn't have a direct 'chains' attribute like OpenMM, 
    # but residues have a 'chain' attribute.
    unique_chain_ids = []
    for residue in item.residues:
        if residue.chain not in unique_chain_ids:
            unique_chain_ids.append(residue.chain)
    n_chains = len(unique_chain_ids)
    chain_id_to_index = {cid: i for i, cid in enumerate(unique_chain_ids)}

    tmp_item = Topology(n_atoms=n_atoms, n_groups=n_groups, n_chains=n_chains)

    # Atoms
    atom_id = []
    atom_name = []
    atom_type = []
    group_index_of_atoms = []

    for atom in item.atoms:
        # ParmEd serials start at 1 usually, number attribute is the serial
        atom_id.append(str(atom.number))
        atom_name.append(atom.name)
        atom_type.append(get_atom_type_from_atom_name(atom.name))
        group_index_of_atoms.append(atom.residue.idx)

    tmp_item.atoms.atom_id = atom_id
    tmp_item.atoms.atom_name = atom_name
    tmp_item.atoms.atom_type = atom_type
    tmp_item.atoms.group_index = group_index_of_atoms

    # Groups
    group_id = []
    group_name = []
    group_type = []
    chain_index_of_groups = []

    for residue in item.residues:
        group_id.append(str(residue.number))
        group_name.append(residue.name)
        group_type.append(get_group_type_from_group_name(residue.name))
        chain_index_of_groups.append(chain_id_to_index[residue.chain])

    tmp_item.groups.group_id = group_id
    tmp_item.groups.group_name = group_name
    tmp_item.groups.group_type = group_type
    tmp_item.groups.chain_index = chain_index_of_groups

    # Chains
    chain_id = []
    chain_name = []
    for cid in unique_chain_ids:
        # If chain is empty string, default to 'A' if it's the only one, or use a label
        label = cid if cid != '' else 'A'
        chain_id.append(str(label))
        chain_name.append(str(label))

    tmp_item.chains.chain_id = chain_id
    tmp_item.chains.chain_name = chain_name

    # Bonds
    if n_bonds > 0:
        bonded_atoms = []
        for bond in item.bonds:
            bonded_atoms.append([bond.atom1.idx, bond.atom2.idx])
        tmp_item.add_bonds(bonded_atoms, skip_digestion=True)

    # Rebuild remaining hierarchy
    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        tmp_item = extract_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
