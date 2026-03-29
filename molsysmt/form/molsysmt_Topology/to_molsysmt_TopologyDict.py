from molsysmt._private.arg_digestion import arg_digest
from molsysmt.native import TopologyDict
import pandas as pd


def _normalize_scalar(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return value


@arg_digest(form='molsysmt.Topology')
def to_molsysmt_TopologyDict(item, skip_digestion=False):
    """Converting Topology to TopologyDict."""

    atoms = []
    for atom_index in range(item.n_atoms):
        row = item.atoms.iloc[atom_index]
        atoms.append({
            'atom_id': None if _normalize_scalar(row['atom_id']) is None else str(_normalize_scalar(row['atom_id'])),
            'atom_name': _normalize_scalar(row['atom_name']),
            'atom_type': _normalize_scalar(row['atom_type']),
        })

    atom_group_index = item.atoms['group_index'].to_numpy(dtype=object)
    groups = []
    for group_index in range(item.n_groups):
        row = item.groups.iloc[group_index]
        groups.append({
            'group_id': None if _normalize_scalar(row['group_id']) is None else str(_normalize_scalar(row['group_id'])),
            'group_name': _normalize_scalar(row['group_name']),
            'group_type': _normalize_scalar(row['group_type']),
            'atom_indices': [int(ii) for ii in range(item.n_atoms) if atom_group_index[ii] == group_index],
        })

    bonds = []
    for bond_index in range(item.n_bonds):
        row = item.bonds.iloc[bond_index]
        bond = {
            'atom_index_1': int(row['atom1_index']),
            'atom_index_2': int(row['atom2_index']),
        }
        if 'order' in item.bonds.columns and _normalize_scalar(row.get('order', None)) is not None:
            bond['bond_order'] = _normalize_scalar(row['order'])
        if 'type' in item.bonds.columns and _normalize_scalar(row.get('type', None)) is not None:
            bond['bond_type'] = _normalize_scalar(row['type'])
        bonds.append(bond)

    chains = []
    if item.n_chains > 0:
        # chain_index is atom-level only; derive per-group from atoms
        if 'chain_index' in item.atoms.columns:
            atom_chain_index = item.atoms['chain_index'].to_numpy(dtype=object)
            group_chain_index = []
            for group_index in range(item.n_groups):
                chain_candidates = [atom_chain_index[ii] for ii in range(item.n_atoms) if atom_group_index[ii] == group_index]
                group_chain_index.append(chain_candidates[0] if chain_candidates else None)
        else:
            group_chain_index = [None] * item.n_groups
        for chain_index in range(item.n_chains):
            row = item.chains.iloc[chain_index]
            chains.append({
                'chain_id': None if _normalize_scalar(row['chain_id']) is None else str(_normalize_scalar(row['chain_id'])),
                'chain_name': _normalize_scalar(row['chain_name']),
                'chain_type': _normalize_scalar(row['chain_type']),
                'group_indices': [int(ii) for ii in range(item.n_groups) if group_chain_index[ii] == chain_index],
            })

    molecules = []
    if item.n_molecules > 0:
        group_molecule_index = item.groups['molecule_index'].to_numpy(dtype=object)
        for molecule_index in range(item.n_molecules):
            row = item.molecules.iloc[molecule_index]
            molecules.append({
                'molecule_id': None if _normalize_scalar(row['molecule_id']) is None else str(_normalize_scalar(row['molecule_id'])),
                'molecule_name': _normalize_scalar(row['molecule_name']),
                'molecule_type': _normalize_scalar(row['molecule_type']),
                'group_indices': [int(ii) for ii in range(item.n_groups) if group_molecule_index[ii] == molecule_index],
            })

    entities = []
    if item.n_entities > 0:
        molecule_entity_index = item.molecules['entity_index'].to_numpy(dtype=object)
        for entity_index in range(item.n_entities):
            row = item.entities.iloc[entity_index]
            entities.append({
                'entity_id': None if _normalize_scalar(row['entity_id']) is None else str(_normalize_scalar(row['entity_id'])),
                'entity_name': _normalize_scalar(row['entity_name']),
                'entity_type': _normalize_scalar(row['entity_type']),
                'molecule_indices': [int(ii) for ii in range(item.n_molecules) if molecule_entity_index[ii] == entity_index],
            })

    return TopologyDict(data={
        'format': 'molsysmt',
        'kind': 'topology',
        'version': '0.1',
        'metadata': {},
        'atoms': atoms,
        'groups': groups,
        'bonds': bonds,
        'chains': chains,
        'molecules': molecules,
        'entities': entities,
    })
