"""Private schema-1 snapshots of stored native mechanics, without rebinding."""

import numbers

import h5py
import numpy as np
import pandas as pd

from .metadata import _prepare_tree, _read_tree, _write_tree

_TEXT = {
    "forcefield",
    "non_bonded_method",
    "constraints",
    "water_model",
    "implicit_solvent",
}
_BOOLEAN = {"dispersion_correction", "flexible_constraints", "rigid_water"}
_NUMBER = {"ewald_error_tolerance", "solute_dielectric", "solvent_dielectric"}
_UNITS = {
    "cutoff_distance": "nm",
    "switch_distance": "nm",
    "hydrogen_mass": "Da",
    "salt_concentration": "mole/liter",
    "kappa": "1/nm",
}
_SETTINGS = _TEXT | _BOOLEAN | _NUMBER | set(_UNITS)
_REPORTS = {"partial_charge_assignment", "atom_type_assignment"}
_COLUMNS = {
    "partial_charge": "elementary_charge",
    "formal_charge": "elementary_charge",
    "atom_ff_type": None,
}
_NULLABLE = {
    f"{kind}{bits}" for kind in ("Int", "UInt") for bits in (8, 16, 32, 64)
} | {"Float32", "Float64"}


def _atom_count(value):
    if (
        isinstance(value, (bool, np.bool_))
        or not isinstance(value, (int, np.integer))
        or value < 0
        or value > np.iinfo(np.int64).max
    ):
        raise ValueError("Mechanics persistence requires a nonnegative atom count.")
    return int(value)


def _quantity_field(path):
    if len(path) != 2 or path[0] != "settings" or path[1] not in _UNITS:
        raise ValueError("A mechanics quantity is outside the declared settings.")
    name = path[1]
    return f"molsysmt.MolecularMechanics/{name}", _UNITS[name]


def _validate_settings(settings):
    from molsysmt import pyunitwizard as puw

    if not isinstance(settings, dict) or set(settings) != _SETTINGS:
        raise ValueError("Unsupported or incomplete mechanics settings.")
    for name, value in settings.items():
        if value is None:
            continue
        if name in _TEXT:
            valid = isinstance(value, str)
        elif name in _BOOLEAN:
            valid = isinstance(value, (bool, np.bool_))
        elif name in _NUMBER:
            valid = isinstance(value, numbers.Real) and not isinstance(
                value, (bool, np.bool_)
            )
            if valid:
                try:
                    valid = bool(np.isfinite(value))
                except TypeError:
                    valid = False
        else:
            valid = not isinstance(
                value, (str, bool, numbers.Number, np.ndarray)
            ) and puw.is_quantity(value)
            if valid:
                valid = puw.get_dimensionality(value) == puw.get_dimensionality(
                    puw.quantity(1.0, _UNITS[name])
                )
            if valid:
                magnitude = np.asarray(puw.get_value(value, to_unit=_UNITS[name]))
                valid = (
                    magnitude.shape == ()
                    and magnitude.dtype.kind in "iuf"
                    and bool(np.isfinite(magnitude))
                )
        if not valid:
            raise ValueError(
                f"Unsupported mechanics setting {name!r}: explicit scalar type and units are required."
            )


def _dtype_descriptor(dtype):
    if isinstance(dtype, pd.StringDtype):
        if dtype.storage != "python":
            raise ValueError("Mechanics string columns require Python-backed storage.")
        return {"kind": "string", "na": "NA" if dtype.na_value is pd.NA else "nan"}
    if isinstance(dtype, np.dtype):
        if (
            dtype.kind not in "iufO"
            or dtype.kind != "O"
            and dtype.itemsize > 8
            or dtype.kind == "f"
            and dtype.itemsize not in {4, 8}
        ):
            raise ValueError("Unsupported mechanics column dtype.")
        return {"kind": "numpy", "name": dtype.str}
    if str(dtype) in _NULLABLE:
        return {"kind": "nullable", "name": str(dtype)}
    raise ValueError("Unsupported mechanics column dtype.")


def _restore_dtype(descriptor):
    if not isinstance(descriptor, dict):
        raise ValueError("Invalid mechanics dtype declaration.")
    if (
        descriptor.get("kind") == "string"
        and set(descriptor) == {"kind", "na"}
        and type(descriptor["na"]) is str
        and descriptor["na"] in {"NA", "nan"}
    ):
        return pd.StringDtype(
            storage="python", na_value=pd.NA if descriptor["na"] == "NA" else np.nan
        )
    if (
        descriptor.get("kind") == "nullable"
        and set(descriptor) == {"kind", "name"}
        and type(descriptor["name"]) is str
        and descriptor["name"] in _NULLABLE
    ):
        return pd.api.types.pandas_dtype(descriptor["name"])
    if (
        descriptor.get("kind") == "numpy"
        and set(descriptor) == {"kind", "name"}
        and type(descriptor["name"]) is str
    ):
        try:
            dtype = np.dtype(descriptor["name"])
        except (ValueError, TypeError) as error:
            raise ValueError("Invalid mechanics NumPy dtype.") from error
        if _dtype_descriptor(dtype) == descriptor:
            return dtype
    raise ValueError("Unsupported mechanics dtype declaration.")


def _null_codes(series):
    codes = np.zeros(len(series), dtype=np.uint8)
    missing = series.isna().to_numpy()
    if series.dtype == np.dtype("object"):
        for index in np.flatnonzero(missing):
            item = series.iloc[index]
            if item is None:
                codes[index] = 1
            elif item is pd.NA:
                codes[index] = 2
            elif isinstance(item, (float, np.floating)) and np.isnan(item):
                codes[index] = 3
    else:
        codes[missing] = 2 if getattr(series.dtype, "na_value", None) is pd.NA else 3
    return codes


def _check_charge_values(name, values):
    if name != "atom_ff_type" and (
        not np.isfinite(values).all()
        or name == "formal_charge"
        and values.dtype.kind == "f"
        and np.any(values != np.trunc(values))
    ):
        raise ValueError(
            "Mechanical charges must be finite; formal charges must be integral."
        )


def _prepare_table(table, n_atoms):
    if table is None:
        return None
    if (
        type(table) is not pd.DataFrame
        or table.attrs
        or not table.flags.allows_duplicate_labels
        or type(table.index) is not pd.RangeIndex
        or table.index.start != 0
        or table.index.step != 1
        or table.index.stop != n_atoms
        or not table.index.equals(pd.RangeIndex(n_atoms))
        or table.index.name is not None
        or table.columns.name is not None
        or not table.columns.is_unique
        or any(name not in _COLUMNS for name in table.columns)
    ):
        raise ValueError("Unsupported mechanics table extension, columns or atom axis.")
    columns = []
    for name in table.columns:
        series = table[name]
        descriptor = _dtype_descriptor(series.dtype)
        codes = _null_codes(series)
        present = codes == 0
        selected = series[present]
        if name == "atom_ff_type":
            if any(not isinstance(item, str) for item in selected):
                raise ValueError("Mechanical atom types must be text or missing.")
            if descriptor["kind"] != "string" and series.dtype != np.dtype("object"):
                raise ValueError("Mechanical atom types need an object/string dtype.")
            values = np.asarray(series.to_numpy(dtype=object, na_value=""), dtype=str)
        else:
            if (
                descriptor["kind"] == "string"
                or series.dtype == np.dtype("object")
                and any(
                    not isinstance(item, numbers.Real)
                    or isinstance(item, (bool, np.bool_))
                    for item in selected
                )
            ):
                raise ValueError("Mechanical charges must be numeric or missing.")
            dtype = (
                np.dtype("int64" if name == "formal_charge" else "float64")
                if series.dtype == np.dtype("object")
                else getattr(series.dtype, "numpy_dtype", series.dtype)
            )
            try:
                values = series.to_numpy(dtype=dtype, na_value=0, copy=True)
                values[~present] = 0
            except (TypeError, ValueError, OverflowError) as error:
                raise ValueError(
                    "Mechanical charge values do not fit their declared storage."
                ) from error
            _check_charge_values(name, values)
            if series.dtype == np.dtype("object") and any(
                value != item for value, item in zip(values[present], selected)
            ):
                raise ValueError("Object charge values would lose numerical precision.")
        columns.append(
            {
                "name": name,
                "dtype": descriptor,
                "unit": _COLUMNS[name],
                "values": values,
                "null_codes": codes,
            }
        )
    return {"n_rows": n_atoms, "columns": columns}


def _read_table(payload, n_atoms):
    if payload is None:
        return None
    if (
        not isinstance(payload, dict)
        or set(payload) != {"n_rows", "columns"}
        or type(payload["n_rows"]) is not int
        or payload["n_rows"] != n_atoms
        or not isinstance(payload["columns"], list)
    ):
        raise ValueError("Invalid mechanics table shape.")
    table = pd.DataFrame(index=pd.RangeIndex(n_atoms))
    for column in payload["columns"]:
        if not isinstance(column, dict) or set(column) != {
            "name",
            "dtype",
            "unit",
            "values",
            "null_codes",
        }:
            raise ValueError("Invalid mechanics column declaration.")
        name = column["name"]
        if (
            type(name) is not str
            or name not in _COLUMNS
            or name in table
            or column["unit"] != _COLUMNS[name]
        ):
            raise ValueError("Unsupported/repeated mechanics column or wrong unit.")
        dtype = _restore_dtype(column["dtype"])
        values, codes = column["values"], column["null_codes"]
        if (
            not isinstance(values, np.ndarray)
            or values.shape != (n_atoms,)
            or not isinstance(codes, np.ndarray)
            or codes.shape != (n_atoms,)
            or codes.dtype != np.dtype("uint8")
            or np.any(codes > 3)
        ):
            raise ValueError("Invalid mechanics values or missing-value codes.")
        if dtype == np.dtype("object"):
            expected = (
                "U"
                if name == "atom_ff_type"
                else "i"
                if name == "formal_charge"
                else "f"
            )
            if (
                values.dtype.kind != expected
                or expected != "U"
                and values.dtype.itemsize != 8
            ):
                raise ValueError("Object column has an incompatible value storage.")
            _check_charge_values(name, values)
            data = values.astype(object)
            data[codes == 1], data[codes == 2], data[codes == 3] = None, pd.NA, np.nan
            series = pd.Series(data, dtype=object)
        else:
            expected_null = 2 if getattr(dtype, "na_value", None) is pd.NA else 3
            if np.any((codes != 0) & (codes != expected_null)):
                raise ValueError("Missing-value policy does not match mechanics dtype.")
            if isinstance(dtype, pd.StringDtype):
                if name != "atom_ff_type" or values.dtype.kind != "U":
                    raise ValueError("String mechanics dtype requires text values.")
            elif name == "atom_ff_type" or values.dtype != getattr(
                dtype, "numpy_dtype", dtype
            ):
                raise ValueError("Numeric mechanics storage does not match its dtype.")
            if isinstance(dtype, np.dtype) and dtype.kind in "iu" and np.any(codes):
                raise ValueError(
                    "Nonnullable integer columns cannot contain missing values."
                )
            _check_charge_values(name, values)
            series = pd.Series(values, dtype=dtype)
            if np.any(codes):
                series.loc[codes != 0] = pd.NA if expected_null == 2 else np.nan
        table[name] = series
    return table


def _prepare_mechanics(mechanics, n_atoms):
    from molsysmt.native.molecular_mechanics import MolecularMechanics

    n_atoms = _atom_count(n_atoms)
    if type(mechanics) is not MolecularMechanics or set(
        vars(mechanics)
    ) != _SETTINGS | _REPORTS | {"atoms_ff"}:
        raise ValueError("Unsupported MolecularMechanics implementation or extension.")
    settings = {name: getattr(mechanics, name) for name in sorted(_SETTINGS)}
    _validate_settings(settings)
    reports = {name: getattr(mechanics, name) for name in sorted(_REPORTS)}
    if any(value is not None and type(value) is not dict for value in reports.values()):
        raise ValueError("Mechanical assignment reports must be detached mappings.")
    payload = {
        "settings": settings,
        "atoms_ff": _prepare_table(mechanics.atoms_ff, n_atoms),
        **reports,
    }
    return _prepare_tree(payload, quantity_field=_quantity_field)


def _validate_destination(root):
    if "molecular_mechanics" in root:
        raise ValueError("The molecular_mechanics layer already exists.")
    kind, version = root.attrs.get("type"), root.attrs.get("version")
    kind = kind.decode() if isinstance(kind, bytes) else kind
    version = version.decode() if isinstance(version, bytes) else version
    if kind == "h5msm" and version not in {
        "0.6",
        "1.0",
    }:
        raise ValueError("This H5MSM version has no molecular mechanics layer.")


def _write_prepared_mechanics(root, prepared, *, n_atoms):
    _validate_destination(root)
    n_atoms = _atom_count(n_atoms)
    group = root.create_group("molecular_mechanics")
    group.attrs["schema_version"] = 1
    group.attrs["n_atoms"] = n_atoms
    _write_tree(group, "snapshot", prepared)


def write_mechanics(root, mechanics, *, n_atoms):
    """Write a private layer after validating all stored fields, without engines."""
    _validate_destination(root)
    n_atoms = _atom_count(n_atoms)
    prepared = _prepare_mechanics(mechanics, n_atoms)
    _write_prepared_mechanics(root, prepared, n_atoms=n_atoms)


def read_mechanics(root, *, n_atoms=None):
    """Restore stored evidence without calculation, repair, migration or binding."""
    from molsysmt.native.molecular_mechanics import MolecularMechanics

    if "molecular_mechanics" not in root:
        return None
    group = root["molecular_mechanics"]
    if (
        not isinstance(group, h5py.Group)
        or set(group.attrs) != {"schema_version", "n_atoms"}
        or np.asarray(group.attrs["schema_version"]).shape != ()
        or np.asarray(group.attrs["schema_version"]).dtype.kind not in "iu"
        or group.attrs["schema_version"] != 1
        or set(group) != {"snapshot"}
    ):
        raise ValueError("Unsupported molecular mechanics layer schema.")
    count = _atom_count(group.attrs["n_atoms"])
    if n_atoms is not None and _atom_count(n_atoms) != count:
        raise ValueError(
            "Mechanical atom count does not match its declared association."
        )
    payload = _read_tree(group["snapshot"], quantity_field=_quantity_field)
    if not isinstance(payload, dict) or set(payload) != {
        "settings",
        "atoms_ff",
        *_REPORTS,
    }:
        raise ValueError("Unsupported mechanics snapshot fields.")
    _validate_settings(payload["settings"])
    if any(
        payload[name] is not None and type(payload[name]) is not dict
        for name in _REPORTS
    ):
        raise ValueError("Mechanical reports must be mappings.")
    restored = MolecularMechanics()
    for name, value in payload["settings"].items():
        setattr(restored, name, value)
    restored.atoms_ff = _read_table(payload["atoms_ff"], count)
    for name in _REPORTS:
        setattr(restored, name, payload[name])
    return restored
