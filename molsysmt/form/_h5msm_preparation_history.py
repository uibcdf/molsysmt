"""Encoding historical preparation evidence with typed HDF5 arrays."""

import json

import h5py
import numpy as np

from molsysmt._private.preparation_history import decode_history, encode_history


def write_history(group, records):
    """Write a compressed manifest and separate arrays, retaining original types."""
    payload = encode_history(records)
    arrays = payload.pop("arrays")
    history = group.create_group("preparation_history")
    history.attrs["schema_version"] = 1
    manifest = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
    history.create_dataset(
        "manifest", data=np.frombuffer(manifest, dtype=np.uint8), compression="gzip"
    )
    table = history.create_group("arrays")
    for key, values in arrays.items():
        options = {"compression": "gzip"} if values.ndim else {}
        if values.dtype.kind == "U":
            dataset = table.create_dataset(
                key, data=values.astype(object), dtype=h5py.string_dtype(), **options
            )
        else:
            dataset = table.create_dataset(key, data=values, **options)
        dataset.attrs["numpy_dtype"] = values.dtype.str


def read_history(group):
    """Read evidence without importing producer software or reporting new work."""
    if "preparation_history" not in group:
        return []
    history = group["preparation_history"]
    if history.attrs.get("schema_version") != 1:
        raise ValueError("Unsupported H5MSM preparation-history schema.")
    manifest = history["manifest"]
    if manifest.ndim != 1 or manifest.dtype != np.dtype("uint8"):
        raise ValueError("Preparation-history manifest must be a byte vector.")
    payload = json.loads(manifest[:].tobytes().decode("utf-8"))
    arrays = {}
    for key, dataset in history["arrays"].items():
        dtype = np.dtype(dataset.attrs["numpy_dtype"])
        if dtype.kind == "U":
            values = np.asarray(dataset.asstr()[()], dtype=dtype)
        else:
            values = np.asarray(dataset[()])
            if values.dtype != dtype:
                raise ValueError("Preparation-history dataset dtype is inconsistent.")
        arrays[key] = values
    payload["arrays"] = arrays
    return decode_history(payload)
