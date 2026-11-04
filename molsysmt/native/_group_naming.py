"""Store explicit group-name declarations independently of chemical assignments."""

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError

# These identifiers version the declaration vocabulary, not complete databases.
PROFILES = (("amber", 1), ("ccd", 1), ("legacy", 1), ("sequence", 1))
NAMES = (None,) + tuple(name for name, _ in PROFILES)


def compact(codes):
    """Own one byte per group only when a declaration is present."""
    if not np.any(codes):
        return None
    result = np.array(codes, dtype=np.uint8, copy=True)
    result.flags.writeable = False
    return result


def stored(topology):
    """Reject stale group axes or unsupported codes before using declarations."""
    codes = getattr(topology, "_group_naming_codes", None)
    if codes is not None and (
        not isinstance(codes, np.ndarray)
        or np.ma.isMaskedArray(codes)
        or codes.dtype != np.dtype("uint8")
        or codes.shape != (topology.n_groups,)
        or np.any(codes >= len(NAMES))
    ):
        raise StructuralInconsistencyError(
            caller="molsysmt.native.Topology",
            reason="Group naming declarations require an aligned uint8 vector with supported profile codes; use coordinated group editing.",
        )
    return codes


def project(topology, group_indices):
    """Transport a validated group map; negative source positions are new groups."""
    codes = stored(topology)
    if codes is None:
        return None
    indices = np.asarray(group_indices, dtype=np.int64)
    known = indices >= 0
    result = np.zeros(len(indices), dtype=np.uint8)
    result[known] = codes[indices[known]]
    return compact(result)


def concatenate(left, right):
    """Keep unknown declarations distinct when joining stable group inventories."""
    first, second = stored(left), stored(right)
    if first is None and second is None:
        return None
    return compact(
        np.concatenate(
            [
                np.zeros(left.n_groups, dtype=np.uint8) if first is None else first,
                np.zeros(right.n_groups, dtype=np.uint8) if second is None else second,
            ]
        )
    )


def extend(topology, count):
    """Stage unknown declarations for newly appended groups before an edit."""
    codes = stored(topology)
    return (
        None
        if codes is None
        else compact(np.concatenate([codes, np.zeros(count, dtype=np.uint8)]))
    )


def encode(topology):
    """Return a versioned, self-describing payload without per-group objects."""
    codes = stored(topology)
    if codes is None:
        return None
    return {
        "schema_version": 1,
        "profiles": [{"name": name, "version": version} for name, version in PROFILES],
        "codes": codes.copy(),
    }


def decode(payload, n_groups):
    """Read only a known declaration registry, never silently reassigning codes."""
    expected = [{"name": name, "version": version} for name, version in PROFILES]
    if (
        not isinstance(payload, dict)
        or set(payload) != {"schema_version", "profiles", "codes"}
        or type(payload["schema_version"]) is not int
        or payload["schema_version"] != 1
        or payload["profiles"] not in (expected[:3], expected)
        or any(type(item.get("version")) is not int for item in payload["profiles"])
    ):
        raise ValueError("Unsupported group naming declaration registry.")
    values = payload["codes"]
    limit = len(payload["profiles"]) + 1
    if isinstance(values, list):
        if any(type(value) is not int or not 0 <= value < limit for value in values):
            raise ValueError("Invalid group naming declaration codes.")
        values = np.asarray(values, dtype=np.uint8)
    if (
        not isinstance(values, np.ndarray)
        or np.ma.isMaskedArray(values)
        or values.dtype != np.dtype("uint8")
        or values.shape != (n_groups,)
        or np.any(values >= limit)
    ):
        raise ValueError("Invalid group naming declaration codes or group alignment.")
    return compact(values)
