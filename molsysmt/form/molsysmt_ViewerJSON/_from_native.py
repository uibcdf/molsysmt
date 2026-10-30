import numpy as np
import pandas as pd

from molsysmt.native import ViewerJSON


def _series_to_list(series):
    """Exporting nullable table scalars as ordinary JSON values."""
    return [
        None
        if pd.isna(value)
        else value.item()
        if isinstance(value, np.generic)
        else value
        for value in series
    ]


def export_native(item, skip_digestion=False, *, chemical_states=None):
    """
    Converting from molsysmt.Topology to molsysmt.ViewerJSON.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.ViewerJSON
        Graphics payload containing ordinary JSON scalars and containers.
        Missing table values become null; bond endpoints are positional indices.

    Notes
    -----
    Per-atom group_index, chain_index and entity_index columns retain distinct
    identities when labels repeat. ID columns remain strings; this graphics
    projection omits molecule metadata and is not a full topology archive.

    Examples
    --------
    >>> import json
    >>> from molsysmt.native import Topology
    >>> topology = Topology(n_atoms=2)
    >>> payload = export_native(topology)
    >>> json.loads(payload.dumps())["bonds"]["atom_pairs"]
    []

    .. versionadded:: 1.0.0
    """

    topo = item
    viewer = ViewerJSON()
    data = viewer.data

    atoms_df = topo.atoms
    groups_df = topo.groups
    molecules_df = topo.molecules
    entities_df = topo.entities
    chains_df = topo.chains

    group_id_map = dict(zip(groups_df.index, _series_to_list(groups_df["group_id"])))
    group_name_map = dict(
        zip(groups_df.index, _series_to_list(groups_df["group_name"]))
    )
    chain_id_map = dict(zip(chains_df.index, _series_to_list(chains_df["chain_id"])))
    mol_index_map = dict(
        zip(groups_df.index, _series_to_list(groups_df["molecule_index"]))
    )
    ent_index_map = dict(
        zip(molecules_df.index, _series_to_list(molecules_df["entity_index"]))
    )
    entity_id_map = dict(
        zip(entities_df.index, _series_to_list(entities_df["entity_id"]))
    )

    atom_group_index = _series_to_list(atoms_df["group_index"])
    atom_chain_index = _series_to_list(atoms_df["chain_index"])

    group_id = [group_id_map.get(ii, None) for ii in atom_group_index]
    group_name = [group_name_map.get(ii, None) for ii in atom_group_index]
    chain_id = [chain_id_map.get(ii, None) for ii in atom_chain_index]

    entity_id = []
    entity_index = []
    for g_idx in atom_group_index:
        if g_idx is None:
            entity_id.append(None)
            entity_index.append(None)
            continue
        mol_idx = mol_index_map.get(g_idx, None)
        if mol_idx is None:
            entity_id.append(None)
            entity_index.append(None)
            continue
        ent_idx = ent_index_map.get(mol_idx, None)
        entity_index.append(ent_idx)
        entity_id.append(entity_id_map.get(ent_idx, None))

    atoms_block = data["atoms"]
    atoms_block["atom_id"] = _series_to_list(atoms_df["atom_id"])
    atoms_block["atom_name"] = _series_to_list(atoms_df["atom_name"])
    atoms_block["group_id"] = group_id
    atoms_block["group_name"] = group_name
    atoms_block["chain_id"] = chain_id
    atoms_block["entity_id"] = entity_id
    # Labels need not be unique. Separate positional columns retain identity.
    atoms_block["group_index"] = atom_group_index
    atoms_block["chain_index"] = atom_chain_index
    atoms_block["entity_index"] = entity_index
    atoms_block["element_symbol"] = _series_to_list(atoms_df["atom_type"])
    formal_charge = (
        None
        if chemical_states is None
        else chemical_states._get_chemical_state_atom_attribute("formal_charge")
    )
    atoms_block["formal_charge"] = (
        [] if formal_charge is None else _series_to_list(formal_charge)
    )

    bonds_df = (
        pd.DataFrame(columns=["atom1_index", "atom2_index"])
        if chemical_states is None
        else chemical_states._get_chemical_state_bonds()
    )
    atom_pairs = list(
        zip(
            _series_to_list(bonds_df["atom1_index"]),
            _series_to_list(bonds_df["atom2_index"]),
        )
    )
    bonds_block = data["bonds"]
    bonds_block["atom_pairs"] = [list(pair) for pair in atom_pairs]
    if "bond_order" in bonds_df:
        bonds_block["order"] = _series_to_list(bonds_df["bond_order"])
    elif "is_aromatic" in bonds_df:
        bonds_block["order"] = [
            "aromatic" if value is not None and bool(value) else None
            for value in _series_to_list(bonds_df["is_aromatic"])
        ]
    else:
        bonds_block["order"] = []
    bonds_block["type"] = (
        _series_to_list(bonds_df["bond_type"]) if "bond_type" in bonds_df else []
    )
    bonds_block["indexA"] = [pair[0] for pair in atom_pairs]
    bonds_block["indexB"] = [pair[1] for pair in atom_pairs]

    data["structures"] = []
    data["frames"] = []

    return viewer
