"""Independent wire guards for the reusable non-executable typed transport."""

import json
from copy import deepcopy

import numpy as np
import pytest

from molsysmt.form._serialization import (
    decode_array,
    decode_typed_tree,
    encode_array,
    encode_typed_tree,
)


@pytest.mark.parametrize(
    "value",
    [
        np.asarray([2**62 + 17, -(2**62)], dtype=">i8"),
        np.asarray([np.nan, np.inf, -np.inf, -0.0], dtype="<f8"),
        np.asarray([[True, False]], dtype=bool),
        np.empty((0, 3), dtype=np.int32),
        np.asarray(12, dtype=np.uint64),
        np.asarray(["alpha", "β"], dtype="<U5"),
    ],
)
def test_array_wire_preserves_exact_shape_dtype_and_bytes(value):
    wire = json.loads(json.dumps(encode_array(value), allow_nan=False))
    restored = decode_array(wire)
    assert restored.shape == value.shape
    assert restored.dtype == value.dtype
    assert restored.tobytes() == value.tobytes()


@pytest.mark.parametrize(
    "field,value",
    [
        ("version", True),
        ("version", 7),
        ("dtype", "O"),
        ("shape", [-1]),
        ("shape", [True]),
        ("shape", [99]),
        ("order", "F"),
        ("encoding", "pickle"),
        ("data", "bad base64"),
    ],
)
def test_invalid_array_envelope_rejects_before_allocation(field, value):
    wire = encode_array(np.asarray([1, 2], dtype=np.int64))
    wire[field] = value
    with pytest.raises(ValueError):
        decode_array(wire)


def test_unicode_values_cannot_silently_truncate():
    wire = encode_array(np.asarray(["abc"], dtype="U3"))
    wire["data"] = ["longer"]
    with pytest.raises(ValueError):
        decode_array(wire)


def test_arbitrary_metadata_markers_are_opaque_and_arrays_are_explicit():
    lookalike = encode_array(np.asarray([99], dtype=np.int64))
    source = {
        "metadata": lookalike,
        "columns": [np.asarray([2**62 + 1], dtype=np.int64)],
    }
    wire = json.loads(json.dumps(encode_typed_tree(source), allow_nan=False))
    output = decode_typed_tree(wire)
    assert output["metadata"] == lookalike
    assert type(output["metadata"]) is dict
    assert output["columns"][0].tolist() == [2**62 + 1]


@pytest.mark.parametrize(
    "fault", ["duplicate", "negative", "missing", "replace", "overlap"]
)
def test_typed_positions_cannot_alias_or_overwrite_metadata(fault):
    wire = encode_typed_tree({"data": [np.asarray([1])], "metadata": 12})
    if fault == "duplicate":
        wire["arrays"].append(deepcopy(wire["arrays"][0]))
    elif fault == "negative":
        wire["arrays"][0]["path"] = ["data", -1]
    elif fault == "missing":
        wire["arrays"][0]["path"] = ["missing"]
    elif fault == "replace":
        wire["arrays"][0]["path"] = ["metadata"]
    else:
        wire["arrays"].append(
            {"path": ["data"], "array": encode_array(np.asarray([2]))}
        )
    with pytest.raises(ValueError):
        decode_typed_tree(wire)


def test_object_arrays_and_cyclic_containers_are_not_a_transport():
    with pytest.raises(ValueError):
        encode_array(np.asarray([object()], dtype=object))
    cyclic = []
    cyclic.append(cyclic)
    with pytest.raises(ValueError):
        encode_typed_tree(cyclic)
