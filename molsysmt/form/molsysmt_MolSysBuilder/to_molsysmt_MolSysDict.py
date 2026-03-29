import numpy as np
import pandas as pd

from molsysmt import pyunitwizard as puw
from molsysmt._private.arg_digestion import arg_digest
from molsysmt.native import MolSysDict


def _normalize_scalar(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return value


def _matches_index(value, index):
    normalized = _normalize_scalar(value)
    return normalized is not None and int(normalized) == index


@arg_digest(form="molsysmt.MolSysBuilder")
def to_molsysmt_MolSysDict(item, skip_digestion=False):
    """Converting MolSysBuilder to MolSysDict without crystallizing declared state."""

    topology = item.topology
    structures = item.structures

    atoms = []
    for atom_index in range(topology.n_atoms):
        row = topology.atoms.iloc[atom_index]
        atoms.append(
            {
                "atom_id": None if _normalize_scalar(row["atom_id"]) is None else str(_normalize_scalar(row["atom_id"])),
                "atom_name": _normalize_scalar(row["atom_name"]),
                "atom_type": _normalize_scalar(row["atom_type"]),
            }
        )

    groups = []
    atom_group_index = topology.atoms["group_index"].to_numpy(dtype=object)
    for group_index in range(topology.n_groups):
        row = topology.groups.iloc[group_index]
        groups.append(
            {
                "group_id": None if _normalize_scalar(row["group_id"]) is None else str(_normalize_scalar(row["group_id"])),
                "group_name": _normalize_scalar(row["group_name"]),
                "group_type": _normalize_scalar(row["group_type"]),
                "atom_indices": [int(ii) for ii in range(topology.n_atoms) if _matches_index(atom_group_index[ii], group_index)],
            }
        )

    bonds = []
    for bond_index in range(topology.n_bonds):
        row = topology.bonds.iloc[bond_index]
        bond = {
            "atom_index_1": int(row["atom1_index"]),
            "atom_index_2": int(row["atom2_index"]),
        }
        if "order" in topology.bonds.columns and _normalize_scalar(row.get("order", None)) is not None:
            bond["bond_order"] = _normalize_scalar(row["order"])
        if "type" in topology.bonds.columns and _normalize_scalar(row.get("type", None)) is not None:
            bond["bond_type"] = _normalize_scalar(row["type"])
        bonds.append(bond)

    chains = []
    if topology.n_chains > 0:
        # chain_index is atom-level only; derive per-group from atoms
        if "chain_index" in topology.atoms.columns:
            _adf = topology.atoms[["group_index", "chain_index"]].dropna()
            _gc = _adf.groupby("group_index", sort=False)["chain_index"].first()
            group_chain_index = np.full(topology.n_groups, None, dtype=object)
            group_chain_index[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy()
        else:
            group_chain_index = np.full(topology.n_groups, None, dtype=object)
        for chain_index in range(topology.n_chains):
            row = topology.chains.iloc[chain_index]
            chains.append(
                {
                    "chain_id": None if _normalize_scalar(row["chain_id"]) is None else str(_normalize_scalar(row["chain_id"])),
                    "chain_name": _normalize_scalar(row["chain_name"]),
                    "chain_type": _normalize_scalar(row["chain_type"]),
                    "group_indices": [int(ii) for ii in range(topology.n_groups) if _matches_index(group_chain_index[ii], chain_index)],
                }
            )

    molecules = []
    if topology.n_molecules > 0:
        group_molecule_index = topology.groups["molecule_index"].to_numpy(dtype=object)
        for molecule_index in range(topology.n_molecules):
            row = topology.molecules.iloc[molecule_index]
            molecules.append(
                {
                    "molecule_id": None if _normalize_scalar(row["molecule_id"]) is None else str(_normalize_scalar(row["molecule_id"])),
                    "molecule_name": _normalize_scalar(row["molecule_name"]),
                    "molecule_type": _normalize_scalar(row["molecule_type"]),
                    "group_indices": [int(ii) for ii in range(topology.n_groups) if _matches_index(group_molecule_index[ii], molecule_index)],
                }
            )

    entities = []
    if topology.n_entities > 0:
        molecule_entity_index = topology.molecules["entity_index"].to_numpy(dtype=object)
        for entity_index in range(topology.n_entities):
            row = topology.entities.iloc[entity_index]
            entities.append(
                {
                    "entity_id": None if _normalize_scalar(row["entity_id"]) is None else str(_normalize_scalar(row["entity_id"])),
                    "entity_name": _normalize_scalar(row["entity_name"]),
                    "entity_type": _normalize_scalar(row["entity_type"]),
                    "molecule_indices": [int(ii) for ii in range(topology.n_molecules) if _matches_index(molecule_entity_index[ii], entity_index)],
                }
            )

    structures_payload = {
        "structure_id": None,
        "time": None,
        "box": None,
        "coordinates": None,
    }
    if structures.structure_id is not None:
        structures_payload["structure_id"] = structures.structure_id.tolist()
    if structures.time is not None:
        structures_payload["time"] = puw.get_value(structures.time, to_unit="ps").tolist()
    if structures.box is not None:
        structures_payload["box"] = puw.get_value(structures.box, to_unit="nm").tolist()
    if structures.coordinates is not None:
        structures_payload["coordinates"] = puw.get_value(structures.coordinates, to_unit="nm").tolist()

    return MolSysDict(
        data={
            "format": "molsysmt",
            "kind": "molsys",
            "version": "0.1",
            "metadata": {},
            "topology": {
                "atoms": atoms,
                "groups": groups,
                "bonds": bonds,
                "chains": chains,
                "molecules": molecules,
                "entities": entities,
            },
            "structures": structures_payload,
        }
    )
