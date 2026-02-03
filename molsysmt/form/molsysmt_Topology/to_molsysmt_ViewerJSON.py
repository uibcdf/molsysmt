from molsysmt._private.arg_digestion import arg_digest
from molsysmt.native import ViewerJSON
import pandas as pd


def _series_to_list(series):
    return [None if pd.isna(ii) else ii for ii in series]


@arg_digest(form='molsysmt.Topology')
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """Converting a native Topology into a ViewerJSON object (no coordinates)."""

    topo = item
    viewer = ViewerJSON()
    data = viewer.data

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

    atoms_block = data["atoms"]
    atoms_block["atom_id"] = _series_to_list(atoms_df['atom_id'])
    atoms_block["atom_name"] = _series_to_list(atoms_df['atom_name'])
    atoms_block["group_id"] = group_id
    atoms_block["group_name"] = group_name
    atoms_block["chain_id"] = chain_id
    atoms_block["entity_id"] = entity_id
    atoms_block["element_symbol"] = _series_to_list(atoms_df['atom_type'])
    atoms_block["formal_charge"] = []

    bonds_df = topo.bonds
    atom_pairs = list(zip(_series_to_list(bonds_df['atom1_index']), _series_to_list(bonds_df['atom2_index'])))
    bonds_block = data["bonds"]
    bonds_block["atom_pairs"] = [list(pair) for pair in atom_pairs]
    bonds_block["order"] = _series_to_list(bonds_df['order']) if 'order' in bonds_df else []
    bonds_block["indexA"] = [pair[0] for pair in atom_pairs]
    bonds_block["indexB"] = [pair[1] for pair in atom_pairs]

    data["structures"] = []
    data["frames"] = []

    return viewer
