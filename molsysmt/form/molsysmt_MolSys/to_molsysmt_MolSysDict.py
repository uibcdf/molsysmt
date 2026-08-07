from molsysmt._private.argdigest import arg_digest
from molsysmt.native import MolSysDict
from molsysmt import pyunitwizard as puw
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


@arg_digest(form='molsysmt.MolSys')
def to_molsysmt_MolSysDict(
    item, atom_indices='all', structure_indices='all', skip_digestion=False
):
    """Converting MolSys to MolSysDict."""

    from .extract import extract

    item = extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )

    atoms = []
    for atom_index in range(item.topology.n_atoms):
        row = item.topology.atoms.iloc[atom_index]
        atoms.append({
            'atom_id': None if _normalize_scalar(row['atom_id']) is None else str(_normalize_scalar(row['atom_id'])),
            'atom_name': _normalize_scalar(row['atom_name']),
            'atom_type': _normalize_scalar(row['atom_type']),
            'isotope': _normalize_scalar(row['isotope']),
        })

    groups = []
    atom_group_index = item.topology.atoms['group_index'].to_numpy(dtype=object)
    for group_index in range(item.topology.n_groups):
        row = item.topology.groups.iloc[group_index]
        groups.append({
            'group_id': None if _normalize_scalar(row['group_id']) is None else str(_normalize_scalar(row['group_id'])),
            'group_name': _normalize_scalar(row['group_name']),
            'group_type': _normalize_scalar(row['group_type']),
            'atom_indices': [int(ii) for ii in range(item.topology.n_atoms) if atom_group_index[ii] == group_index],
        })

    bonds = []
    bonds_df = item.topology._get_chemical_state_bonds()
    if bonds_df.shape[0] > 0:
        for bond_index in range(bonds_df.shape[0]):
            row = bonds_df.iloc[bond_index]
            bond = {
                'atom_index_1': int(row['atom1_index']),
                'atom_index_2': int(row['atom2_index']),
            }
            if 'bond_order' in bonds_df.columns and _normalize_scalar(row.get('bond_order', None)) is not None:
                bond['bond_order'] = _normalize_scalar(row['bond_order'])
            elif (
                'is_aromatic' in bonds_df.columns
                and _normalize_scalar(row.get('is_aromatic', None)) is not None
                and bool(row['is_aromatic'])
            ):
                bond['bond_order'] = 'aromatic'
            if 'bond_type' in bonds_df.columns and _normalize_scalar(row.get('bond_type', None)) is not None:
                bond['bond_type'] = _normalize_scalar(row['bond_type'])
            bonds.append(bond)

    chains = []
    if item.topology.n_chains > 0:
        # chain_index is atom-level only; derive per-group from atoms
        if 'chain_index' in item.topology.atoms.columns:
            atom_chain_index = item.topology.atoms['chain_index'].to_numpy(dtype=object)
            group_chain_index = []
            for group_index in range(item.topology.n_groups):
                chain_candidates = [atom_chain_index[ii] for ii in range(item.topology.n_atoms) if atom_group_index[ii] == group_index]
                group_chain_index.append(chain_candidates[0] if chain_candidates else None)
        else:
            group_chain_index = [None] * item.topology.n_groups

        for chain_index in range(item.topology.n_chains):
            row = item.topology.chains.iloc[chain_index]
            chains.append({
                'chain_id': None if _normalize_scalar(row['chain_id']) is None else str(_normalize_scalar(row['chain_id'])),
                'chain_name': _normalize_scalar(row['chain_name']),
                'chain_type': _normalize_scalar(row['chain_type']),
                'group_indices': [int(ii) for ii in range(item.topology.n_groups) if group_chain_index[ii] == chain_index],
            })

    molecules = []
    if item.topology.n_molecules > 0:
        group_molecule_index = item.topology.groups['molecule_index'].to_numpy(dtype=object)
        for molecule_index in range(item.topology.n_molecules):
            row = item.topology.molecules.iloc[molecule_index]
            molecules.append({
                'molecule_id': None if _normalize_scalar(row['molecule_id']) is None else str(_normalize_scalar(row['molecule_id'])),
                'molecule_name': _normalize_scalar(row['molecule_name']),
                'molecule_type': _normalize_scalar(row['molecule_type']),
                'group_indices': [int(ii) for ii in range(item.topology.n_groups) if group_molecule_index[ii] == molecule_index],
            })

    entities = []
    if item.topology.n_entities > 0:
        molecule_entity_index = item.topology.molecules['entity_index'].to_numpy(dtype=object)
        for entity_index in range(item.topology.n_entities):
            row = item.topology.entities.iloc[entity_index]
            entities.append({
                'entity_id': None if _normalize_scalar(row['entity_id']) is None else str(_normalize_scalar(row['entity_id'])),
                'entity_name': _normalize_scalar(row['entity_name']),
                'entity_type': _normalize_scalar(row['entity_type']),
                'molecule_indices': [int(ii) for ii in range(item.topology.n_molecules) if molecule_entity_index[ii] == entity_index],
            })

    structures = {
        'structure_id': None,
        'time': None,
        'box': None,
        'coordinates': None,
    }

    if item.structures.structure_id is not None:
        structures['structure_id'] = item.structures.structure_id.tolist()
    if item.structures.time is not None:
        structures['time'] = puw.get_value(item.structures.time, to_unit='ps').tolist()
    if item.structures.box is not None:
        structures['box'] = puw.get_value(item.structures.box, to_unit='nm').tolist()
    if item.structures.coordinates is not None:
        structures['coordinates'] = puw.get_value(item.structures.coordinates, to_unit='nm').tolist()

    data = {
        'format': 'molsysmt',
        'kind': 'molsys',
        'version': '0.1',
        'metadata': {},
        'topology': {
            'atoms': atoms,
            'groups': groups,
            'bonds': bonds,
            'chains': chains,
            'molecules': molecules,
            'entities': entities,
        },
        'structures': structures,
    }

    return MolSysDict(data=data)
