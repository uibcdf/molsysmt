"""Columnar dictionary form for discrete chemical states."""

from copy import deepcopy
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ChemicalStatesDict:
    """Holding a lossless, versioned chemical-state payload.

    State tables are stored as typed columns with explicit null masks. The
    representation uses NumPy arrays and is not directly JSON serializable.
    """

    data: dict

    def to_dict(self, copy=True):
        """Returning the underlying typed payload."""

        return deepcopy(self.data) if copy else self.data

    def copy(self):
        """Returning an independent typed payload."""

        return ChemicalStatesDict(deepcopy(self.data))


def _encode_series(series):
    dtype = str(series.dtype)
    null_mask = series.isna().to_numpy(dtype=np.bool_)
    if dtype in {"string", "object", "str"}:
        values = series.fillna("").astype(str).to_numpy(dtype=np.str_)
    elif dtype in {"boolean", "bool"}:
        values = series.fillna(False).to_numpy(dtype=np.bool_)
    elif dtype.startswith(("Int", "UInt", "Float")):
        values = series.fillna(0).to_numpy(dtype=np.dtype(dtype.lower()))
    else:
        values = series.to_numpy(copy=True)
        if values.dtype.kind not in "iufbUS":
            raise ValueError(f"Unsupported ChemicalStatesDict dtype {dtype!r}.")
    return {"dtype": dtype, "values": values, "null_mask": null_mask}


def _decode_series(payload):
    values = np.asarray(payload["values"])
    null_mask = np.asarray(payload["null_mask"], dtype=np.bool_)
    if values.ndim != 1 or null_mask.shape != values.shape:
        raise ValueError("ChemicalStatesDict column values and null mask differ.")
    result = pd.Series(pd.array(values.copy(), dtype=payload["dtype"]))
    if null_mask.any():
        result.loc[null_mask] = pd.NA
    return result


def _encode_table(table):
    return {
        "n_rows": len(table),
        "columns": {name: _encode_series(table[name]) for name in table.columns},
    }


def _decode_table(payload):
    n_rows = int(payload["n_rows"])
    table = pd.DataFrame(index=range(n_rows))
    for name, column in payload["columns"].items():
        series = _decode_series(column)
        if len(series) != n_rows:
            raise ValueError("ChemicalStatesDict table column has the wrong length.")
        table[name] = series
    return table


def _encode_chemical_states(states):
    records = []
    for state in states._states:
        records.append(
            {
                "state_id": state.state_id,
                "connectivity_completeness": state.connectivity_completeness,
                "component_completeness": state.component_completeness,
                "component_evidence": state.component_evidence,
                "provenance_index": state.provenance_index,
                "component_indices": _encode_series(state.component_indices),
                "components": _encode_table(state.components),
                "atom_attributes": _encode_table(state.atom_attributes),
                "bonds": _encode_table(state.bonds),
            }
        )
    return ChemicalStatesDict(
        {
            "schema": "molsysmt.chemical_states_dict",
            "version": 1,
            "n_atoms": states.n_atoms,
            "reference_chemical_state_index": states._reference_index,
            "states": records,
        }
    )


def _decode_chemical_states(payload):
    from .chemical_states import ChemicalStates
    from .topology import Bonds_DataFrame, Components_DataFrame, _ChemicalStateStorage

    data = payload.data
    if (
        data.get("schema") != "molsysmt.chemical_states_dict"
        or data.get("version") != 1
    ):
        raise ValueError("Unsupported ChemicalStatesDict schema or version.")
    n_atoms = int(data["n_atoms"])
    collection = ChemicalStates(n_atoms=n_atoms)
    records = []
    for record in data["states"]:
        components_table = _decode_table(record["components"])
        components = Components_DataFrame(n_components=len(components_table))
        for name in components_table:
            components[name] = components_table[name]

        bonds_table = _decode_table(record["bonds"])
        bonds = Bonds_DataFrame(n_bonds=len(bonds_table))
        for name in bonds_table:
            bonds[name] = bonds_table[name]

        component_indices = _decode_series(record["component_indices"])
        if len(component_indices) != n_atoms:
            raise ValueError(
                "ChemicalStatesDict component indices have the wrong length."
            )
        state = _ChemicalStateStorage(
            n_atoms=n_atoms,
            bonds=bonds,
            components=components,
            component_indices=component_indices,
            state_id=record["state_id"],
            connectivity_completeness=record["connectivity_completeness"],
            component_completeness=record["component_completeness"],
            component_evidence=record["component_evidence"],
            provenance_index=record["provenance_index"],
        )
        state.atom_attributes = _decode_table(record["atom_attributes"])
        state._ensure_compatibility(n_atoms)
        records.append(state)
    collection._replace_states(records, data["reference_chemical_state_index"])
    return collection
