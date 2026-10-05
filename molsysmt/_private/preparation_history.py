"""Preserving preparation evidence in the original operation's index domains."""

from copy import deepcopy

import numpy as np


def validate_history(records):
    """Check historical envelopes without interpreting their scientific payload."""
    if not isinstance(records, (list, tuple)):
        raise ValueError("Preparation history must be a list or tuple of records.")
    for record in records:
        if (
            not isinstance(record, dict)
            or set(record) != {"schema", "index_scope", "output", "report"}
            or record["schema"] != "molsysmt.preparation_record@1"
            or record["index_scope"] != "operation"
        ):
            raise ValueError("Unsupported preparation record schema or index scope.")
        output = record["output"]
        if not isinstance(output, dict) or set(output) != {
            "n_atoms",
            "n_bonds",
            "chemical_state_index",
        }:
            raise ValueError("Preparation records require original output dimensions.")
        for value in output.values():
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(
                    "Preparation output dimensions must be nonnegative integers."
                )
        report = record["report"]
        if not isinstance(report, dict) or not isinstance(report.get("schema"), str):
            raise ValueError("Preparation reports require a provider-owned schema.")


def append_report(state, report, chemical_state_index):
    """Append original evidence; do not create another chemical assignment store."""
    record = dict(
        schema="molsysmt.preparation_record@1",
        index_scope="operation",
        output=dict(
            n_atoms=len(state.atom_attributes),
            n_bonds=len(state.bonds),
            chemical_state_index=int(chemical_state_index),
        ),
        report=deepcopy(report),
    )
    validate_history([record])
    state._preparation_history.append(record)


def remap_bond_history_references(table, records, offset):
    """Offset known local history references without reinterpreting opaque origins."""
    if not offset or "provenance_index" not in table:
        return table
    local = {
        index
        for index, record in enumerate(records)
        if record["report"]["schema"]
        in {
            "molsysmt.pdb_connectivity@1",
            "molsysmt.covalent_inference@1",
        }
    }
    mask = table["provenance_index"].isin(local)
    if not mask.any():
        return table
    output = table.copy()
    output.loc[mask, "provenance_index"] += offset
    return output


def encode_history(records, *, copy_arrays=True):
    """Encode a typed tree and separate arrays without pickle or object arrays."""
    validate_history(records)
    arrays = {}

    def encode(value):
        if isinstance(value, np.ndarray):
            if value.dtype.kind not in "biufUS":
                raise ValueError("Unsupported preparation-history array dtype.")
            key = str(len(arrays))
            arrays[key] = value.copy() if copy_arrays else value
            return dict(
                kind="array", key=key, dtype=value.dtype.str, shape=list(value.shape)
            )
        if isinstance(value, np.generic):
            value = value.item()
        if value is None or isinstance(value, (str, bool, int, float)):
            if isinstance(value, float) and not np.isfinite(value):
                raise ValueError("Preparation-history scalar values must be finite.")
            return dict(kind="scalar", value=value)
        if isinstance(value, dict):
            if any(not isinstance(key, str) for key in value):
                raise ValueError("Preparation-history mapping keys must be strings.")
            return dict(
                kind="dict", items=[[key, encode(item)] for key, item in value.items()]
            )
        if isinstance(value, (list, tuple)):
            return dict(
                kind="tuple" if isinstance(value, tuple) else "list",
                items=[encode(item) for item in value],
            )
        raise ValueError(
            f"Unsupported preparation-history value type {type(value).__name__!r}."
        )

    return dict(
        schema="molsysmt.preparation_history",
        version=1,
        tree=encode(list(records)),
        arrays=arrays,
    )


def decode_history(payload):
    """Decode only declared types, rejecting inconsistent array references."""
    if (
        payload.get("schema") != "molsysmt.preparation_history"
        or payload.get("version") != 1
    ):
        raise ValueError("Unsupported preparation-history serialization schema.")
    arrays = payload["arrays"]
    used = set()

    def decode(node):
        kind = node.get("kind")
        if kind == "scalar" and set(node) == {"kind", "value"}:
            value = node["value"]
            if value is None or isinstance(value, (str, bool, int, float)):
                if not isinstance(value, float) or np.isfinite(value):
                    return value
        elif kind == "array" and set(node) == {"kind", "key", "dtype", "shape"}:
            key = node["key"]
            value = np.asarray(arrays[key])
            if (
                value.dtype.kind not in "biufUS"
                or value.dtype.str != node["dtype"]
                or list(value.shape) != node["shape"]
                or key in used
            ):
                raise ValueError(
                    "Preparation-history array dtype, shape or reference is inconsistent."
                )
            used.add(key)
            return value.copy()
        elif kind in {"list", "tuple", "dict"} and set(node) == {"kind", "items"}:
            items = node["items"]
            if kind == "dict":
                result = {}
                for key, value in items:
                    if not isinstance(key, str) or key in result:
                        raise ValueError(
                            "Preparation-history mapping keys must be unique strings."
                        )
                    result[key] = decode(value)
                return result
            result = [decode(item) for item in items]
            return tuple(result) if kind == "tuple" else result
        raise ValueError("Unsupported preparation-history tree node.")

    records = decode(payload["tree"])
    if used != set(arrays):
        raise ValueError("Preparation history contains unreferenced arrays.")
    validate_history(records)
    return records
