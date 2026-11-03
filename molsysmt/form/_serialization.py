"""Normalizing primitive values at declarative serialization boundaries."""

from collections.abc import Mapping

import numpy as np
import pandas as pd


def encode_array(value):
    """Encode a non-object array without discarding dtype, shape or integer bits."""
    import base64

    value = np.asarray(value)
    if value.dtype.kind not in "biufU" or value.dtype.fields is not None:
        raise ValueError(
            "Typed transport supports numeric, boolean and Unicode arrays only."
        )
    return {
        "__molsysmt_transport__": "ndarray",
        "version": 1,
        "dtype": value.dtype.str,
        "shape": list(value.shape),
        "order": "C",
        "encoding": "strings" if value.dtype.kind == "U" else "base64",
        "data": value.ravel(order="C").tolist()
        if value.dtype.kind == "U"
        else base64.b64encode(value.tobytes(order="C")).decode("ascii"),
    }


def decode_array(record):
    """Validate every envelope field and byte count before creating an array."""
    import base64
    from math import prod

    keys = {
        "__molsysmt_transport__",
        "version",
        "dtype",
        "shape",
        "order",
        "encoding",
        "data",
    }
    if (
        not isinstance(record, dict)
        or set(record) != keys
        or record["__molsysmt_transport__"] != "ndarray"
        or type(record["version"]) is not int
        or record["version"] != 1
        or record["order"] != "C"
        or not isinstance(record["dtype"], str)
    ):
        raise ValueError("Invalid or unsupported typed-array envelope.")
    shape = record["shape"]
    if not isinstance(shape, list) or any(type(n) is not int or n < 0 for n in shape):
        raise ValueError("Typed-array dimensions must be nonnegative integers.")
    try:
        dtype = np.dtype(record["dtype"])
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid typed-array dtype.") from error
    if dtype.kind not in "biufU" or dtype.fields is not None or dtype.itemsize == 0:
        raise ValueError("Unsupported typed-array dtype.")
    count = prod(shape)
    data = record["data"]
    if dtype.kind == "U":
        if (
            record["encoding"] != "strings"
            or not isinstance(data, list)
            or len(data) != count
            or any(not isinstance(v, str) or len(v) > dtype.itemsize // 4 for v in data)
        ):
            raise ValueError("Typed Unicode values do not match their dtype and shape.")
        return np.asarray(data, dtype=dtype).reshape(shape)
    if record["encoding"] != "base64" or not isinstance(data, str):
        raise ValueError("Numeric typed arrays require base64 bytes.")
    try:
        raw = base64.b64decode(data, validate=True)
    except (ValueError, UnicodeError) as error:
        raise ValueError("Invalid typed-array base64 data.") from error
    if len(raw) != count * dtype.itemsize:
        raise ValueError("Typed-array byte count does not match dtype and shape.")
    return np.frombuffer(raw, dtype=dtype).reshape(shape)


def encode_typed_tree(value, *, quantity_field=None):
    """Declare typed leaf positions separately from uninterpreted metadata mappings.

    A metadata mapping that happens to resemble an array envelope stays a mapping.
    Only positions explicitly listed by this transport are decoded as typed leaves.
    Quantity fields use PyUnitWizard's sealed record rather than a second unit codec.
    """
    from molsysmt import pyunitwizard as puw

    arrays, quantities, active = [], [], set()

    def visit(node, path):
        if not isinstance(
            node, (str, bool, int, float, np.generic, Mapping, list, tuple)
        ) and puw.is_quantity(node):
            if quantity_field is None:
                raise ValueError("This domain does not admit untyped quantity leaves.")
            from pyunitwizard.record import QuantityRecord

            field, _ = quantity_field(path)
            quantities.append(
                {
                    "path": path,
                    "record": QuantityRecord.from_quantity(node, field=field).to_dict(),
                }
            )
            return None
        if isinstance(node, np.ndarray):
            arrays.append({"path": path, "array": encode_array(node)})
            return None
        if isinstance(node, np.generic):
            return visit(node.item(), path)
        if node is None or isinstance(node, (str, bool, int)):
            return node
        if isinstance(node, float):
            if not np.isfinite(node):
                raise ValueError(
                    "Nonfinite scalar metadata needs an explicitly typed array."
                )
            return node
        if isinstance(node, (Mapping, list, tuple)):
            if id(node) in active:
                raise ValueError("Declarative transport cannot encode cyclic metadata.")
            active.add(id(node))
            try:
                if isinstance(node, Mapping):
                    if any(not isinstance(key, str) for key in node):
                        raise ValueError(
                            "Typed transport mapping keys must be strings."
                        )
                    return {
                        key: visit(child, path + [key]) for key, child in node.items()
                    }
                return [
                    visit(child, path + [index]) for index, child in enumerate(node)
                ]
            finally:
                active.remove(id(node))
        raise ValueError(f"Unsupported declarative value at {path!r}.")

    plain = visit(value, [])
    return {
        "__molsysmt_transport__": "tree",
        "version": 1,
        "value": plain,
        "arrays": arrays,
        "quantities": quantities,
    }


def decode_typed_tree(payload, *, quantity_field=None):
    """Decode only declared typed positions, never scanning metadata for markers."""
    from copy import deepcopy

    if (
        not isinstance(payload, dict)
        or set(payload)
        != {"__molsysmt_transport__", "version", "value", "arrays", "quantities"}
        or payload["__molsysmt_transport__"] != "tree"
        or type(payload["version"]) is not int
        or payload["version"] != 1
        or not isinstance(payload["arrays"], list)
        or not isinstance(payload["quantities"], list)
    ):
        raise ValueError("Invalid or unsupported typed-tree envelope.")
    value = deepcopy(payload["value"])
    seen = set()

    def place(path, replacement):
        nonlocal value
        if not isinstance(path, list) or any(
            type(key) not in {str, int} for key in path
        ):
            raise ValueError("Invalid typed-leaf path.")
        key = tuple(path)
        if key in seen or any(
            key[: len(old)] == old or old[: len(key)] == key for old in seen
        ):
            raise ValueError("Typed-leaf paths overlap or repeat.")
        seen.add(key)
        if not path:
            if value is not None:
                raise ValueError("Typed-leaf placeholder must be None.")
            value = replacement
            return
        parent = value
        try:
            for key in path[:-1]:
                if (
                    isinstance(parent, list)
                    and (type(key) is not int or key < 0)
                    or isinstance(parent, dict)
                    and not isinstance(key, str)
                    or not isinstance(parent, (list, dict))
                ):
                    raise ValueError("Invalid typed-leaf parent.")
                parent = parent[key]
            key = path[-1]
            if (
                isinstance(parent, list)
                and (type(key) is not int or key < 0)
                or isinstance(parent, dict)
                and not isinstance(key, str)
                or not isinstance(parent, (list, dict))
                or parent[key] is not None
            ):
                raise ValueError("Typed-leaf placeholder must be None.")
            parent[key] = replacement
        except (IndexError, KeyError, TypeError) as error:
            raise ValueError(
                "Typed-leaf path is outside its declared container."
            ) from error

    for entry in payload["arrays"]:
        if not isinstance(entry, dict) or set(entry) != {"path", "array"}:
            raise ValueError("Invalid typed-array position declaration.")
        place(entry["path"], decode_array(entry["array"]))
    for entry in payload["quantities"]:
        if (
            quantity_field is None
            or not isinstance(entry, dict)
            or set(entry) != {"path", "record"}
        ):
            raise ValueError("Invalid or unsupported quantity position declaration.")
        from pyunitwizard.record import QuantityRecord

        field, unit = quantity_field(entry["path"])
        place(
            entry["path"],
            QuantityRecord.from_dict(entry["record"]).to_quantity(
                field=field, unit=unit
            ),
        )
    return value


def normalize_scalar(value):
    """Represent nullable table scalars as Python primitives or None."""
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return value.item() if isinstance(value, np.generic) else value


def to_builtin(value):
    """Convert dimensionless containers and NumPy scalars to safe YAML values."""
    if isinstance(value, Mapping):
        return {to_builtin(key): to_builtin(item) for key, item in value.items()}
    if isinstance(value, np.ndarray):
        return to_builtin(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [to_builtin(item) for item in value]
    return value
