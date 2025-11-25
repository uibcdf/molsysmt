from molsysmt._private.digestion import digest
from molsysmt.native import ViewerJSON
from molsysmt import pyunitwizard as puw
import pandas as pd
import numpy as np


def _series_to_list(series):
    return [None if pd.isna(ii) else ii for ii in series]


def _angles_from_box(box):
    # box: (3,3) matrix
    a_vec, b_vec, c_vec = box
    a = np.linalg.norm(a_vec)
    b = np.linalg.norm(b_vec)
    c = np.linalg.norm(c_vec)
    alpha = np.degrees(np.arccos(np.dot(b_vec, c_vec) / (b * c)))
    beta = np.degrees(np.arccos(np.dot(a_vec, c_vec) / (a * c)))
    gamma = np.degrees(np.arccos(np.dot(a_vec, b_vec) / (a * b)))
    return dict(a=float(a), b=float(b), c=float(c), alpha=float(alpha), beta=float(beta), gamma=float(gamma))


@digest(form='molsysmt.MolSys')
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """Convert a native MolSys into a ViewerJSON container."""

    topo = item.topology
    structs = item.structures

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

    # entity ids per atom
    group_to_entity = []
    for g_idx in atom_group_index:
        if g_idx is None:
            group_to_entity.append(None)
            continue
        mol_idx = mol_index_map.get(g_idx, None)
        if mol_idx is None:
            group_to_entity.append(None)
            continue
        ent_idx = ent_index_map.get(mol_idx, None)
        group_to_entity.append(entity_id_map.get(ent_idx, None))

    atoms_block = {
        "atom_id": _series_to_list(atoms_df['atom_id']),
        "atom_name": _series_to_list(atoms_df['atom_name']),
        "group_id": group_id,
        "group_name": group_name,
        "chain_id": chain_id,
        "entity_id": group_to_entity,
        "element_symbol": [],  # placeholder if absent
        "formal_charge": [],
    }

    bonds_df = topo.bonds
    bonds_block = {
        "indexA": _series_to_list(bonds_df['atom1_index']),
        "indexB": _series_to_list(bonds_df['atom2_index']),
        "order": _series_to_list(bonds_df['order']) if 'order' in bonds_df else [],
    }

    frames = []
    coords = structs.coordinates
    times = structs.time
    boxes = structs.box

    coords_values = puw.get_value(coords, to_unit='nanometer') if coords is not None else None
    time_values = puw.get_value(times, to_unit='picosecond') if times is not None else None
    box_values = puw.get_value(boxes, to_unit='nanometer') if boxes is not None else None

    if coords_values is not None:
        for ii, positions in enumerate(coords_values):
            frame = {"positions": np.asarray(positions, dtype=float).tolist()}
            if time_values is not None:
                frame["time"] = float(time_values[ii])
            if box_values is not None:
                frame["cell"] = _angles_from_box(np.asarray(box_values[ii]))
            frames.append(frame)

    data = {
        "version": "0.1",
        "atoms": atoms_block,
        "bonds": bonds_block,
        "estructures": frames,
    }

    return ViewerJSON(data=data)
