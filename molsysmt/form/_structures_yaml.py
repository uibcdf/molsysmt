"""Versioned quantity and sparse-site boundaries for structures YAML."""

from collections.abc import Mapping

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import FormatError

QUANTITY_FIELDS = {
    "coordinates": "nm",
    "box": "nm",
    "time": "ps",
    "velocities": "nm/ps",
    "b_factor": "nm**2",
}
_SITE_FIELDS = {"location_id", "atom_id", "occupancy", "coordinates", "b_factor"}


def _invalid(reason):
    return FormatError(reason=f"Structures YAML: {reason}", caller="molsysmt.convert")


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


def quantity_record(value, field, unit, *, reading=False):
    """Use the provider codec and an explicit field/unit handshake."""
    from pyunitwizard.record import QuantityRecord, RecordError

    try:
        if reading:
            return QuantityRecord.from_dict(value).to_quantity(field=field, unit=unit)
        record = QuantityRecord.from_quantity(value, field=field, unit=unit)
        encoding = "base64" if not np.isfinite(record.values).all() else "json"
        return record.to_dict(encoding=encoding)
    except (RecordError, TypeError, ValueError, KeyError, OverflowError) as error:
        raise _invalid(
            f"invalid quantity for {field!r}; expected {unit!r}: {error}"
        ) from error


def alternate_sites(value, coordinates, *, reading=False, version="0.2"):
    """Validate sparse sites while encoding or decoding their quantity fields."""
    if not isinstance(value, (list, tuple, np.ndarray)):
        raise _invalid("alternate_location must be a sequence of structure mappings.")
    n_atoms = None
    if coordinates is not None:
        shape = np.shape(puw.get_value(coordinates, to_unit="nm"))
        if len(shape) != 3 or shape[-1] != 3 or len(value) != shape[0]:
            raise _invalid(
                "alternate sites do not match the coordinate structure axis."
            )
        n_atoms = shape[1]
    output = []
    for structure_index, sites in enumerate(value):
        if not isinstance(sites, Mapping):
            raise _invalid(f"alternate structure {structure_index} is not a mapping.")
        selected = {}
        for index, entry in sites.items():
            if (
                not isinstance(index, (int, np.integer))
                or isinstance(index, (bool, np.bool_))
                or index < 0
                or (n_atoms is not None and index >= n_atoms)
            ):
                raise _invalid(
                    f"invalid alternate atom index {index!r} in structure {structure_index}."
                )
            if not isinstance(entry, Mapping) or set(entry) - _SITE_FIELDS:
                raise _invalid(f"invalid alternate-site fields for atom index {index}.")
            location = entry.get("location_id")
            if (
                not isinstance(location, (list, tuple, np.ndarray))
                or np.ndim(location) != 1
            ):
                raise _invalid(
                    f"alternate atom index {index} requires a sequence of location labels."
                )
            location = list(location)
            if not location or any(not isinstance(label, str) for label in location):
                raise _invalid(
                    f"invalid location labels for alternate atom index {index}."
                )
            count = len(location)
            result = {
                "location_id": np.asarray(location)
                if reading
                else [str(label) for label in location]
            }
            ids = entry.get("atom_id")
            if ids is not None:
                if (
                    not isinstance(ids, (list, tuple, np.ndarray))
                    or np.ndim(ids) != 1
                    or len(ids) != count
                ):
                    raise _invalid(
                        f"atom ID count does not match alternate sites at atom index {index}."
                    )
                ids = [None if label is None else str(label) for label in ids]
            result["atom_id"] = ids
            occupancy = entry.get("occupancy")
            if occupancy is not None:
                try:
                    occupancy = np.asarray(occupancy, dtype=float)
                except (TypeError, ValueError) as error:
                    raise _invalid(
                        f"invalid occupancy at atom index {index}."
                    ) from error
                if occupancy.shape != (count,):
                    raise _invalid(
                        f"occupancy count does not match alternate sites at atom index {index}."
                    )
            result["occupancy"] = occupancy if reading else to_builtin(occupancy)
            for name, unit, shape in (
                ("coordinates", "nm", (count, 3)),
                ("b_factor", "nm**2", (count,)),
            ):
                quantity = entry.get(name)
                field = f"alternate_location.{name}"
                if quantity is not None:
                    if reading and version == "0.1":
                        raise _invalid(
                            f"legacy alternate {name!r} has no negotiated unit; use a 0.2 quantity record."
                        )
                    decoded = (
                        quantity_record(quantity, field, unit, reading=True)
                        if reading
                        else quantity
                    )
                    if not puw.is_quantity(decoded):
                        raise _invalid(
                            f"alternate {name!r} at atom index {index} requires units of {unit!r}."
                        )
                    try:
                        values = puw.get_value(decoded, to_unit=unit)
                    except (TypeError, ValueError) as error:
                        raise _invalid(
                            f"alternate {name!r} requires units of {unit!r}."
                        ) from error
                    if np.shape(values) != shape:
                        raise _invalid(
                            f"alternate {name!r} at atom index {index} must have shape {shape}."
                        )
                    if name == "coordinates" and not np.isfinite(values).all():
                        raise _invalid(
                            f"alternate coordinates at atom index {index} must be finite."
                        )
                    quantity = (
                        decoded if reading else quantity_record(decoded, field, unit)
                    )
                result[name] = quantity
            selected[int(index)] = result
        output.append(selected)
    return output


def encode_structures(item):
    """Encode the supported structural payload in schema 0.2."""
    payload = {}
    for name, unit in QUANTITY_FIELDS.items():
        value = item.get(name)
        if value is not None:
            payload[name] = quantity_record(value, f"structures.{name}", unit)
    for name in ("structure_id", "occupancy"):
        if item.get(name) is not None:
            payload[name] = to_builtin(item[name])
    if item.get("alternate_location") is not None:
        payload["alternate_location"] = alternate_sites(
            item["alternate_location"], item.get("coordinates")
        )
    return {
        "format": "molsysmt",
        "kind": "structures",
        "version": "0.2",
        "metadata": {},
        "structures": payload,
    }


def decode_structures(data):
    """Read 0.1 canonical fields or verified 0.2 quantity records."""
    if (
        not isinstance(data, Mapping)
        or data.get("format") != "molsysmt"
        or data.get("kind") != "structures"
    ):
        raise _invalid("expected a molsysmt structures document.")
    version = data.get("version")
    if version not in ("0.1", "0.2"):
        raise _invalid(
            f"unsupported schema version {version!r}; expected '0.1' or '0.2'."
        )
    payload = data.get("structures")
    if not isinstance(payload, Mapping):
        raise _invalid("structures must be a mapping.")
    output = {}
    for name, unit in QUANTITY_FIELDS.items():
        value = payload.get(name)
        if value is not None:
            output[name] = (
                quantity_record(value, f"structures.{name}", unit, reading=True)
                if version == "0.2"
                else puw.quantity(value, unit)
            )
    if payload.get("structure_id") is not None:
        output["structure_id"] = payload["structure_id"]
    if payload.get("occupancy") is not None:
        output["occupancy"] = np.asarray(payload["occupancy"])
    if payload.get("alternate_location") is not None:
        output["alternate_location"] = alternate_sites(
            payload["alternate_location"],
            output.get("coordinates"),
            reading=True,
            version=version,
        )
    return output
