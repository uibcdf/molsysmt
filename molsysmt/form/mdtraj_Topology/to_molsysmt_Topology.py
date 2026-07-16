from molsysmt._private.arg_digestion import arg_digest
from molsysmt.element.group import get_group_type_from_group_name
import numpy as np
import pandas as pd

@arg_digest(form='mdtraj.Topology')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt._private.variables import is_all

    if hasattr(item, 'topology'):
        item = item.topology

    n_atoms = item.n_atoms
    n_groups = item.n_residues
    n_chains = item.n_chains

    tmp_item = Topology(n_atoms=n_atoms, n_groups=n_groups, n_chains=n_chains)

    # Atoms and Groups
    atom_id = []
    atom_name = []
    atom_type = []
    group_id = []
    group_name = []
    group_type = []
    group_index_of_atoms = []

    for atom in item.atoms:
        atom_id.append(str(atom.serial))
        atom_name.append(atom.name)
        atom_type.append(atom.element.symbol if atom.element else None)
        group_index_of_atoms.append(atom.residue.index)

    formal_charge = [
        pd.NA if getattr(atom, 'formal_charge', None) is None else int(atom.formal_charge)
        for atom in item.atoms
    ]

    for residue in item.residues:
        group_id.append(str(residue.resSeq))
        group_name.append(residue.name)
        group_type.append(get_group_type_from_group_name(residue.name))

    tmp_item.atoms['atom_id'] = atom_id
    tmp_item.atoms['atom_name'] = atom_name
    tmp_item.atoms['atom_type'] = atom_type
    tmp_item.atoms['group_index'] = group_index_of_atoms
    tmp_item._set_chemical_state_atom_attribute('formal_charge', formal_charge)

    tmp_item.groups['group_id'] = group_id
    tmp_item.groups['group_name'] = group_name
    tmp_item.groups['group_type'] = group_type

    # Bonds
    bonds = list(item.bonds)
    if bonds:
        type_names = [str(getattr(bond, 'type', '')).lower() for bond in bonds]
        tmp_item._append_chemical_state_bonds(
            [[bond.atom1.index, bond.atom2.index] for bond in bonds],
            bond_order=[
                pd.NA if getattr(bond, 'order', None) is None else int(bond.order)
                for bond in bonds
            ],
            bond_type=['covalent'] * len(bonds),
            is_aromatic=['aromatic' in value for value in type_names],
            evidence=['explicit'] * len(bonds),
        )
    tmp_item._chemical_states[0].connectivity_completeness = 'complete'

    # Chains
    chain_id = []
    chain_name = []
    group_index_of_chains = [[] for _ in range(n_chains)]
    for residue in item.residues:
        group_index_of_chains[residue.chain.index].append(residue.index)
    
    for chain in item.chains:
        chain_id.append(str(chain.chain_id if hasattr(chain, 'chain_id') else chain.index))
        chain_name.append(str(chain.index))

    tmp_item.chains['chain_id'] = chain_id
    tmp_item.chains['chain_name'] = chain_name
    # chain_index lives on atoms only
    chain_index_of_groups = np.zeros(n_groups, dtype=int)
    for ii in range(n_chains):
        for jj in group_index_of_chains[ii]:
            chain_index_of_groups[jj] = ii
    atom_group_arr = np.array(group_index_of_atoms, dtype=int)
    tmp_item.atoms['chain_index'] = chain_index_of_groups[atom_group_arr]

    # Rebuild metadata
    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
