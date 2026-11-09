"""Preserving declarative metadata with numeric arrays outside the JSON tree."""

import json
from dataclasses import dataclass
from math import prod

import h5py
import numpy as np

_WINDOW = 256 * 1024


@dataclass(frozen=True)
class _PreparedTree:
    text: bytes
    arrays: tuple


def _array_dtype(value):
    dtype = np.dtype(value)
    if (
        dtype.fields is not None
        or dtype.kind not in "biufU"
        or not dtype.itemsize
        or dtype.kind != "U"
        and dtype.itemsize > 8
    ):
        raise ValueError("Unsupported declarative HDF5 array dtype.")
    return dtype


def _prepare_tree(value, *, quantity_field=None):
    """Validate the whole tree before creating any HDF5 objects."""
    from molsysmt import pyunitwizard as puw

    arrays, active = [], set()

    def visit(node, path):
        if isinstance(node, (np.ndarray, np.generic)):
            if (
                isinstance(node, np.ndarray)
                and type(node) is not np.ndarray
                or isinstance(node, np.generic)
                and type(node) is not node.dtype.type
            ):
                raise ValueError("Array/scalar subclasses require an explicit schema.")
            array = np.asarray(node)
            _array_dtype(array.dtype)
            if array.dtype.kind == "U":
                for item in array.flat:
                    if "\x00" in str(item):
                        raise ValueError("HDF5 Unicode arrays cannot contain NUL.")
                    try:
                        str(item).encode("utf-8")
                    except UnicodeError as error:
                        raise ValueError("Invalid UTF-8 array label.") from error
            index = len(arrays)
            arrays.append(array)
            return {
                "type": "numpy_scalar" if isinstance(node, np.generic) else "array",
                "index": index,
                "dtype": array.dtype.str,
                "shape": list(array.shape),
            }
        if node is None or type(node) in {str, bool, int, float}:
            if type(node) is float and not np.isfinite(node):
                raise ValueError("Nonfinite metadata requires an explicit array.")
            return {"type": "scalar", "value": node}
        if type(node) in {dict, list, tuple}:
            if id(node) in active:
                raise ValueError("Declarative HDF5 metadata cannot contain cycles.")
            active.add(id(node))
            try:
                if type(node) is dict:
                    if any(type(key) is not str for key in node):
                        raise ValueError("Metadata mapping keys must be strings.")
                    children = [
                        [key, visit(item, path + [key])] for key, item in node.items()
                    ]
                    return {"type": "mapping", "items": children}
                return {
                    "type": "tuple" if type(node) is tuple else "list",
                    "items": [
                        visit(item, path + [index]) for index, item in enumerate(node)
                    ],
                }
            finally:
                active.remove(id(node))
        # Text that happens to parse as a quantity remains literal text above.
        if quantity_field is not None and puw.is_quantity(node):
            from pyunitwizard.record import QuantityRecord

            field, unit = quantity_field(path)
            record = QuantityRecord.from_quantity(node, field=field)
            record.to_quantity(
                field=field,
                dimensionality=puw.get_dimensionality(puw.quantity(1.0, unit)),
            )
            return {"type": "quantity", "record": record.to_dict()}
        raise ValueError(f"Unsupported declarative metadata at {path!r}.")

    try:
        text = json.dumps(
            visit(value, []), allow_nan=False, separators=(",", ":")
        ).encode("utf-8")
    except RecursionError as error:
        raise ValueError("Declarative metadata nesting is too deep.") from error
    return _PreparedTree(text, tuple(arrays))


def _write_array(group, name, array):
    """Transfer numeric data and bounded UTF-8 byte blocks without object heaps."""
    dtype = (
        h5py.string_dtype("utf-8", length=array.dtype.itemsize)
        if array.dtype.kind == "U"
        else array.dtype
    )
    options = {"compression": "gzip"} if array.ndim and array.size else {}
    dataset = group.create_dataset(name, shape=array.shape, dtype=dtype, **options)
    if not array.ndim:
        dataset[()] = (
            np.asarray(str(array.item()).encode("utf-8"), dtype=dtype)
            if array.dtype.kind == "U"
            else array[()]
        )
    else:
        rows = max(1, _WINDOW // max(1, prod(array.shape[1:]) * array.dtype.itemsize))
        for start in range(0, len(array), rows):
            block = array[start : start + rows]
            dataset[start : start + rows] = (
                np.char.encode(block, "utf-8").astype(dtype)
                if array.dtype.kind == "U"
                else block
            )


def _write_tree(parent, name, prepared):
    group = parent.create_group(name)
    group.attrs["schema_version"] = 1
    group.create_dataset("json", data=np.frombuffer(prepared.text, dtype=np.uint8))
    arrays = group.create_group("arrays")
    for index, array in enumerate(prepared.arrays):
        _write_array(arrays, str(index), array)


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Repeated metadata JSON key.")
        result[key] = value
    return result


def _read_tree(group, *, quantity_field=None):
    """Read only explicit node types, never infer types from metadata contents."""
    if (
        not isinstance(group, h5py.Group)
        or set(group.attrs) != {"schema_version"}
        or np.asarray(group.attrs["schema_version"]).shape != ()
        or np.asarray(group.attrs["schema_version"]).dtype.kind not in "iu"
        or group.attrs["schema_version"] != 1
        or set(group) != {"json", "arrays"}
        or not isinstance(group["arrays"], h5py.Group)
        or group["arrays"].attrs
    ):
        raise ValueError("Unsupported declarative HDF5 metadata schema.")
    dataset = group["json"]
    if (
        not isinstance(dataset, h5py.Dataset)
        or dataset.dtype != np.dtype("uint8")
        or dataset.ndim != 1
        or dataset.attrs
    ):
        raise ValueError("Invalid declarative metadata JSON dataset.")
    try:
        tree = json.loads(dataset[:].tobytes(), object_pairs_hook=_unique_pairs)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("Invalid declarative metadata JSON.") from error
    used = set()

    def visit(node, path):
        if not isinstance(node, dict) or type(node.get("type")) is not str:
            raise ValueError("Invalid declarative metadata node.")
        kind = node["type"]
        if kind == "scalar" and set(node) == {"type", "value"}:
            value = node["value"]
            if (
                value is None
                or type(value) in {str, bool, int}
                or type(value) is float
                and np.isfinite(value)
            ):
                return value
        elif (
            kind in {"mapping", "list", "tuple"}
            and set(node) == {"type", "items"}
            and isinstance(node["items"], list)
        ):
            if kind == "mapping":
                result = {}
                for entry in node["items"]:
                    if (
                        not isinstance(entry, list)
                        or len(entry) != 2
                        or type(entry[0]) is not str
                        or entry[0] in result
                    ):
                        raise ValueError("Invalid or repeated metadata mapping key.")
                    result[entry[0]] = visit(entry[1], path + [entry[0]])
                return result
            values = [
                visit(item, path + [index]) for index, item in enumerate(node["items"])
            ]
            return tuple(values) if kind == "tuple" else values
        elif kind in {"array", "numpy_scalar"} and set(node) == {
            "type",
            "index",
            "dtype",
            "shape",
        }:
            index, shape = node["index"], node["shape"]
            if (
                type(index) is not int
                or index < 0
                or index in used
                or not isinstance(shape, list)
                or any(type(n) is not int or n < 0 for n in shape)
            ):
                raise ValueError("Invalid metadata array reference.")
            if type(node["dtype"]) is not str:
                raise ValueError("Metadata array dtype must be an explicit string.")
            dtype = _array_dtype(node["dtype"])
            if str(index) not in group["arrays"]:
                raise ValueError("Missing metadata array dataset.")
            source = group["arrays"][str(index)]
            if (
                not isinstance(source, h5py.Dataset)
                or source.shape != tuple(shape)
                or source.attrs
            ):
                raise ValueError("Metadata array shape does not match its declaration.")
            if dtype.kind == "U":
                string = h5py.check_string_dtype(source.dtype)
                if string is None or string.encoding != "utf-8":
                    raise ValueError("Metadata Unicode array requires UTF-8 storage.")
                values = source.asstr()[()]
                if any(
                    len(str(item)) > dtype.itemsize // 4
                    for item in np.asarray(values).flat
                ):
                    raise ValueError("Metadata Unicode values exceed declared width.")
                array = np.asarray(values, dtype=dtype)
            else:
                if source.dtype != dtype:
                    raise ValueError(
                        "Metadata array dtype does not match its declaration."
                    )
                array = np.asarray(source[()], dtype=dtype)
            used.add(index)
            if kind == "numpy_scalar":
                if array.shape:
                    raise ValueError("A NumPy scalar requires a scalar dataset.")
                return array[()]
            return array
        elif (
            kind == "quantity"
            and set(node) == {"type", "record"}
            and quantity_field is not None
        ):
            from pyunitwizard.record import QuantityRecord

            from molsysmt import pyunitwizard as puw

            field, unit = quantity_field(path)
            return QuantityRecord.from_dict(node["record"]).to_quantity(
                field=field,
                dimensionality=puw.get_dimensionality(puw.quantity(1.0, unit)),
            )
        raise ValueError("Unsupported declarative metadata node.")

    try:
        result = visit(tree, [])
    except RecursionError as error:
        raise ValueError("Declarative metadata nesting is too deep.") from error
    if set(group["arrays"]) != {str(index) for index in used}:
        raise ValueError("Unreferenced metadata arrays cannot be discarded.")
    return result
