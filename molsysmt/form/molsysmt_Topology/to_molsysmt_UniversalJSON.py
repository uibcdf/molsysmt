from molsysmt._private.digestion import digest
from molsysmt.native import UniversalJSON
import pandas as pd


def _series_to_list(series):
    return [None if pd.isna(ii) else ii for ii in series]


@digest(form='molsysmt.Topology')
def to_molsysmt_UniversalJSON(item, skip_digestion=False):
    """Convert a native Topology into a UniversalJSON object (topology only)."""

    topo = item
    atoms_df = topo.atoms
    groups_df = topo.groups
    molecules_df = topo.molecules
    entities_df = topo.entities
    chains_df = topo.chains

    group_id_map = dict(zip(groups_df.index, _series_to_list(groups_df['group_id'])))
    group_name_map = dict(zip(groups_df.index, _series_to_list(groups_df['group_name'])))
    chain_id_map = dict(zip(chains_df.index, _series_to_list(chains_df['chain_id'])))
    mol_index_map = dict(zip(groups_df.index, _series_to_list(groups_df['molecule_index'])))
    ent_index_map = dict(zip(molecules_df.index, _series_to_list(molecules_df['entity_index'])))
    entity_id_map = dict(zip(entities_df.index, _series_to_list(entities_df['entity_id'])))

    atom_group_index = _series_to_list(atoms_df['group_index'])
    atom_chain_index = _series_to_list(atoms_df['chain_index'])

    group_id = [group_id_map.get(ii, None) for ii in atom_group_index]
    group_name = [group_name_map.get(ii, None) for ii in atom_group_index]
    chain_id = [chain_id_map.get(ii, None) for ii in atom_chain_index]

    entity_id = []
    for g_idx in atom_group_index:
        if g_idx is None:
            entity_id.append(None)
            continue
        mol_idx = mol_index_map.get(g_idx, None)
        if mol_idx is None:
            entity_id.append(None)
            continue
        ent_idx = ent_index_map.get(mol_idx, None)
        entity_id.append(entity_id_map.get(ent_idx, None))

    atoms_block = {
        "atom_id": _series_to_list(atoms_df['atom_id']),
        "atom_name": _series_to_list(atoms_df['atom_name']),
        "group_id": group_id,
        "group_name": group_name,
        "chain_id": chain_id,
        "entity_id": entity_id,
        "element_symbol": [],
        "formal_charge": [],
    }

    bonds_df = topo.bonds
    bonds_block = {
        "indexA": _series_to_list(bonds_df['atom1_index']),
        "indexB": _series_to_list(bonds_df['atom2_index']),
        "order": _series_to_list(bonds_df['order']) if 'order' in bonds_df else [],
    }

    data = {
        "version": "0.1",
        "topology": {"atoms": atoms_block},
        "bonds": bonds_block,
        "coordinates": {"collections": [{"label": "default", "estructures": []}]},
        "metadata": {},
        "annotations": {},
    }

    return UniversalJSON(data=data)
