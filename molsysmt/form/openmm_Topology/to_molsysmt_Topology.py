from molsysmt._private.arg_digestion import arg_digest
from molsysmt.element.group import get_group_type_from_group_name
import numpy as np
import pandas as pd

@arg_digest(form='openmm.Topology')
def to_molsysmt_Topology(item, atom_indices='all', get_missing_bonds=True, skip_digestion=False):

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
    chain_index_of_atoms = []
    
    group_id = []
    group_name = []
    group_type = []
    chain_index_of_groups = []

    for atom in item.atoms():
        atom_id.append(str(atom.id))
        atom_name.append(atom.name)
        atom_type.append(atom.element.symbol if atom.element else None)
        group_index_of_atoms.append(atom.residue.index)
        chain_index_of_atoms.append(atom.residue.chain.index)

    formal_charge = [
        pd.NA if getattr(atom, 'formalCharge', None) is None else int(atom.formalCharge)
        for atom in item.atoms()
    ]

    for residue in item.residues():
        group_id.append(str(residue.id))
        group_name.append(residue.name)
        group_type.append(get_group_type_from_group_name(residue.name))
        chain_index_of_groups.append(residue.chain.index)

    tmp_item.atoms['atom_id'] = atom_id
    tmp_item.atoms['atom_name'] = atom_name
    tmp_item.atoms['atom_type'] = atom_type
    tmp_item.atoms['group_index'] = group_index_of_atoms
    tmp_item.atoms['chain_index'] = chain_index_of_atoms
    tmp_item._set_chemical_state_atom_attribute('formal_charge', formal_charge)

    tmp_item.groups['group_id'] = group_id
    tmp_item.groups['group_name'] = group_name
    tmp_item.groups['group_type'] = group_type

    # Chains
    chain_id = []
    chain_name = []
    for chain in item.chains():
        chain_id.append(str(chain.id))
        chain_name.append(str(chain.id))

    tmp_item.chains['chain_id'] = chain_id
    tmp_item.chains['chain_name'] = chain_name

    # Bonds
    if n_bonds > 0:
        bonds = list(item.bonds())
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
    elif get_missing_bonds:
        from molsysmt.build import get_missing_bonds as _get_missing_bonds
        try:
            # We try to get bonds using MolSysMT's internal heuristics
            # This works well for water/ions even without coordinates if names are standard
            bonded_atoms = _get_missing_bonds(item, skip_digestion=True)
            if bonded_atoms is not None and len(bonded_atoms)>0:
                tmp_item._append_chemical_state_bonds(
                    bonded_atoms, evidence=['inferred'] * len(bonded_atoms)
                )
                tmp_item._chemical_states[0].connectivity_completeness = 'partial'
        except Exception:
            pass
    else:
        tmp_item._chemical_states[0].connectivity_completeness = 'complete'

    # Rebuild remaining hierarchy
    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()
    tmp_item.rebuild_chains(redefine_indices=False, redefine_ids=False, redefine_names=False, redefine_types=True)

    if not is_all(atom_indices):
        tmp_item = extract_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
