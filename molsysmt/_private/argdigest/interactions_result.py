"""Argument digesters for the typed sparse-result boundary.

The explicit registry keeps local sparse index semantics separate from general
molecular-system selections. Cross-column and scientific invariants stay in the
result constructor, including when decoding trusted typed payloads.
"""

from collections.abc import Iterable, Mapping

import numpy as np

from molsysmt._private.smonitor import ArgumentError
from molsysmt.interactions._query_modes import QUERY_MODES

from .argument.filename import digest_filename
from .argument.replacement import digest_replacement
from .argument.skip_digestion import digest_skip_digestion


def _bind(function, **options):
    def digest(value, caller=None):
        return function(value, caller=caller, **options)

    return digest


def _count(value, caller=None, *, name, optional=False):
    if optional and value is None:
        return None
    if (
        isinstance(value, (bool, np.bool_))
        or not isinstance(value, (int, np.integer))
        or value < 0
    ):
        raise ArgumentError(
            name,
            value=value,
            caller=caller,
            message=f"{name} must be a nonnegative integer",
        )
    return int(value)


def _integer_array(value, caller=None, *, name, optional=False, ndim=1, scalar=False):
    if optional and value is None:
        return None
    array = np.asarray(value)
    if scalar and array.ndim == 0:
        array = array.reshape(1)
    # Empty selections have no values to coerce. Typed storage columns still
    # declare integer dtypes; Python sequences need a canonical empty dtype.
    if array.size == 0 and (scalar or isinstance(value, (list, tuple, range))):
        array = np.asarray(value, dtype=np.int64)
    if array.ndim != ndim or array.dtype.kind not in "iu":
        raise ValueError(f"{name} must be a {ndim}-dimensional array of integers")
    dtype = np.int32 if name in {"image_vectors", "occurrence_evidence"} else np.int64
    bounds = np.iinfo(dtype)
    if (
        array.size
        and not np.can_cast(array.dtype, dtype, casting="safe")
        and (np.any(array < bounds.min) or np.any(array > bounds.max))
    ):
        raise ValueError(
            f"{name} contains an integer outside the {np.dtype(dtype)} range"
        )
    return array


def _indices(value, caller=None, *, name):
    from molsysmt._private.variables import is_all

    method = caller.rsplit(".", 1)[-1]
    if method == "remap" and is_all(value):
        return "all"
    if (
        method in {"query", "between_selections"}
        and value is None
        and name not in {"atom_indices_a", "atom_indices_b"}
    ):
        return None
    array = np.asarray(value)
    if array.ndim == 0:
        array = array.reshape(1)
    if not array.size:
        array = array.astype(np.int64, copy=False)
    return _integer_array(array, name=name)


def _strings(value, caller=None, *, name, optional=False, single=False):
    if optional and value is None:
        return None
    if single and isinstance(value, str):
        return value
    if isinstance(value, str):
        raise ArgumentError(name, value=value, caller=caller)
    try:
        result = tuple(value)
    except TypeError as error:
        raise ArgumentError(name, value=value, caller=caller) from error
    if any(not isinstance(item, str) for item in result):
        raise ArgumentError(name, value=value, caller=caller)
    return result


def _mapping(value, caller=None, *, name, optional=False):
    if optional and value is None:
        return None
    if not isinstance(value, Mapping) or any(not isinstance(key, str) for key in value):
        raise ArgumentError(name, value=value, caller=caller)
    return value


def _iterable(value, caller=None, *, name, optional=False):
    if optional and value is None:
        return None
    if isinstance(value, (str, bytes, Mapping)):
        raise ArgumentError(name, value=value, caller=caller)
    if not isinstance(value, Iterable) and not hasattr(type(value), "__getitem__"):
        raise ArgumentError(name, value=value, caller=caller)
    return value


def _text(value, caller=None, *, name, optional=False):
    if optional and value is None:
        return None
    if not isinstance(value, str) or (name == "method" and not value.strip()):
        raise ArgumentError(name, value=value, caller=caller)
    return value


def _choice(value, caller=None, *, name, choices):
    if not isinstance(value, str) or value not in choices:
        raise ValueError(f"{name} must be one of {choices}")
    return value


def _boolean(value, caller=None, *, name):
    if not isinstance(value, bool):
        raise ArgumentError(name, value=value, caller=caller)
    return value


def _relation_index(value, caller=None):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ArgumentError("relation_index", value=value, caller=caller)
    return int(value)


def _class(cls, caller=None):
    from molsysmt.interactions.result import Interactions

    if not isinstance(cls, type) or not issubclass(cls, Interactions):
        raise ArgumentError("cls", value=cls, caller=caller)
    return cls


def _software(value, caller=None):
    from molsysmt.interactions.result import _software_versions

    return _software_versions(value)


ARGUMENT_DIGESTERS = {
    "cls": _class,
    "skip_digestion": digest_skip_digestion,
    "filename": digest_filename,
    "replacement": digest_replacement,
    "relation_index": _relation_index,
    "records": _bind(_iterable, name="records"),
    "execution_records": _bind(_iterable, name="execution_records", optional=True),
    "method": _bind(_text, name="method"),
    "source_id": _bind(_text, name="source_id", optional=True),
    "exclusive": _bind(_boolean, name="exclusive"),
    "mode": _bind(_choice, name="mode", choices=QUERY_MODES),
    "evaluation_mode": _bind(
        _choice, name="evaluation_mode", choices=("internal", "incident", "between")
    ),
    "interaction_types": _bind(
        _strings, name="interaction_types", optional=True, single=True
    ),
}
for _name in ("n_atoms", "n_structures", "source_n_atoms", "source_n_structures"):
    ARGUMENT_DIGESTERS[_name] = _bind(
        _count, name=_name, optional=_name.startswith("source_")
    )
for _name in ("atom_indices", "structure_indices", "atom_indices_a", "atom_indices_b"):
    ARGUMENT_DIGESTERS[_name] = _bind(_indices, name=_name)
for _name in ("relation_types", "participant_roles", "evidence_labels"):
    ARGUMENT_DIGESTERS[_name] = _bind(
        _strings, name=_name, optional=_name == "evidence_labels"
    )
for _name in ("measurements", "measure_units", "parameters", "software", "execution"):
    ARGUMENT_DIGESTERS[_name] = _bind(
        _mapping, name=_name, optional=_name != "measurements"
    )
ARGUMENT_DIGESTERS["software"] = _software
for _name in (
    "evaluated_structure_indices",
    "relation_participant_offsets",
    "participant_atom_offsets",
    "participant_atoms",
    "occurrence_structures",
    "occurrence_relations",
    "occurrence_image_offsets",
    "atom_source_indices",
    "structure_source_indices",
    "evaluation_atom_indices",
    "evaluation_atom_indices_b",
    "evaluation_universe_indices",
    "image_vectors",
):
    ARGUMENT_DIGESTERS[_name] = _bind(
        _integer_array,
        name=_name,
        ndim=2 if _name == "image_vectors" else 1,
        optional=_name
        in {
            "occurrence_image_offsets",
            "atom_source_indices",
            "structure_source_indices",
            "evaluation_atom_indices",
            "evaluation_atom_indices_b",
            "evaluation_universe_indices",
            "image_vectors",
        },
        scalar=_name
        in {
            "evaluated_structure_indices",
            "evaluation_atom_indices",
            "evaluation_atom_indices_b",
            "evaluation_universe_indices",
        },
    )


def _evidence(occurrence_evidence, evidence_labels=None, caller=None):
    if evidence_labels is None:
        return _strings(occurrence_evidence, name="occurrence_evidence", caller=caller)
    return _integer_array(
        occurrence_evidence, name="occurrence_evidence", caller=caller
    )


ARGUMENT_DIGESTERS["occurrence_evidence"] = _evidence
