"""Read requested chemical columns without decoding or caching native states."""

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.variables import is_all
from molsysmt.basic._index_validation import validate_element_indices

from ._chemical_fields import ATOM_FIELDS, BOND_FIELDS, COMPONENT_FIELDS, project_fields
from ._chemical_queries import project_arrays
from ._chemical_scope import active_index
from ._chemical_state import (
    _BOND_OPTIONAL_DTYPES,
    _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES,
)


def _bad(reason):
    raise StructuralInconsistencyError(
        reason=reason, caller="molsysmt.ChemicalStatesDict.get"
    )


def _integer(value, name):
    if (
        isinstance(value, (bool, np.bool_))
        or not isinstance(value, (int, np.integer))
        or value < 0
    ):
        _bad(f"ChemicalStatesDict {name} must be a nonnegative integer.")
    return int(value)


def header(item):
    """Validate collection metadata without visiting unrequested state records."""
    data = item.data
    if (
        not isinstance(data, dict)
        or data.get("schema") != "molsysmt.chemical_states_dict"
    ):
        _bad("Unsupported ChemicalStatesDict schema or version.")
    if _integer(data.get("version"), "version") not in {1, 2}:
        _bad("Unsupported ChemicalStatesDict schema or version.")
    atoms = _integer(data.get("n_atoms"), "n_atoms")
    records = data.get("states")
    if not isinstance(records, list):
        _bad("ChemicalStatesDict states must be an ordered list.")
    reference = data.get("reference_chemical_state_index")
    if reference is not None:
        reference = _integer(reference, "reference_chemical_state_index")
        if reference >= len(records):
            _bad("ChemicalStatesDict reference is outside its state inventory.")
    return data, atoms, len(records), 0 if len(records) == 1 else reference


def _state(item):
    data = header(item)[0]
    index = item._resolve_index(active_index(item))
    record = data["states"][index]
    if not isinstance(record, dict):
        _bad("The selected chemical-state record must be a dictionary.")
    return record


def _table(state, name):
    table = state.get(name)
    if not isinstance(table, dict) or not isinstance(table.get("columns"), dict):
        _bad(f"ChemicalStatesDict table {name!r} is not a typed column table.")
    return table, _integer(table.get("n_rows"), name + " row count")


def _raw(column, size, expected):
    if (
        not isinstance(column, dict)
        or not isinstance(column.get("dtype"), str)
        or column["dtype"] not in expected
    ):
        _bad("ChemicalStatesDict column dtype does not match its chemical field.")
    from molsysmt import pyunitwizard as puw

    if puw.is_quantity(column.get("values")):
        _bad("Typed chemical columns require fixed-schema magnitudes, not quantities.")
    values = np.asarray(column.get("values"))
    mask = np.asarray(column.get("null_mask"))
    if (
        values.ndim != 1
        or len(values) != size
        or mask.shape != values.shape
        or mask.dtype.kind != "b"
    ):
        _bad("ChemicalStatesDict values, null mask and declared row count disagree.")
    return values, mask, column["dtype"]


def _expected(table, name):
    if table == "components":
        return {"string", "object", "str"}
    if table == "atom_attributes":
        return {_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name]}
    return {
        "Int64"
        if name in {"atom1_index", "atom2_index"}
        else _BOND_OPTIONAL_DTYPES[name]
    }


def _arrays(column, size, expected, positions=None):
    values, mask, dtype = _raw(column, size, expected)
    if positions is not None:
        values, mask = values[positions], mask[positions]
    present = values[~mask]
    if dtype in {"string", "object", "str"}:
        if any(not isinstance(value, (str, np.str_)) for value in present):
            _bad("ChemicalStatesDict label values must be strings.")
    elif dtype == "boolean":
        if values.dtype.kind != "b":
            _bad("ChemicalStatesDict boolean values must be boolean arrays.")
    else:
        numeric = np.dtype(dtype.lower())
        if values.dtype.kind not in "iuf" or not np.all(np.isfinite(present)):
            _bad("ChemicalStatesDict numerical values must be finite magnitudes.")
        if numeric.kind in "iu":
            limits = np.iinfo(numeric)
            if (
                np.any(present < limits.min)
                or np.any(present > limits.max)
                or np.any(present != np.floor(present))
            ):
                _bad("ChemicalStatesDict integer values exceed their declared dtype.")
        # Null placeholders carry no value: do not cast an arbitrary masked cell.
        normalized = np.zeros(len(values), dtype=numeric)
        normalized[~mask] = present
        values = normalized
    return values, mask


def _column(state, table_name, name, positions, size):
    table, count = _table(state, table_name)
    if name not in table["columns"]:
        return [None] * size
    values, mask = _arrays(
        table["columns"][name], count, _expected(table_name, name), positions
    )
    output = values.tolist()
    for index in np.flatnonzero(mask):
        output[index] = None
    return output


def _membership(item, state, positions=None):
    atoms = header(item)[1]
    values, mask = _arrays(state.get("component_indices"), atoms, {"Int64"}, positions)
    count = _table(state, "components")[1]
    if np.any(values[~mask] < 0) or np.any(values[~mask] >= count):
        _bad(
            "Stored component membership does not match the chemical atom/component axes."
        )
    values = values.copy()
    values[mask] = -1
    return values


def _pairs(item, state):
    _, count = _table(state, "bonds")
    columns = []
    for name in ("atom1_index", "atom2_index"):
        if name not in state["bonds"]["columns"]:
            _bad("Stored bonds require both endpoint columns.")
        values, mask = _arrays(state["bonds"]["columns"][name], count, {"Int64"})
        if mask.any() or np.any(values < 0) or np.any(values >= header(item)[1]):
            _bad("Stored bond endpoints are outside the chemical atom domain.")
        columns.append(values)
    return np.column_stack(columns)


def count(item, element):
    if element == "atom":
        return header(item)[1]
    return _table(_state(item), "bonds" if element == "bond" else "components")[1]


def _positions(item, element, selected):
    size = count(item, element)
    return validate_element_indices(
        item,
        selected,
        element,
        "indices",
        "chemical dictionary query",
        count_getter=lambda _: size,
    )


def system(item, attribute):
    data, atoms, size, reference = header(item)
    if attribute == "n_atoms":
        return atoms
    if attribute == "n_chemical_states":
        return size
    if attribute == "chemical_state_index":
        return list(range(size))
    if attribute == "chemical_state_id":
        return [
            None if record.get("state_id") is None else str(record["state_id"])
            for record in data["states"]
        ]
    if attribute == "reference_chemical_state_index":
        return reference
    if attribute in {"n_bonds", "n_components"}:
        return count(item, "bond" if attribute == "n_bonds" else "component")
    value = _state(item).get(attribute)
    choices = (
        {"explicit", "inferred", "user_defined", "unknown"}
        if attribute == "component_evidence"
        else {"unavailable", "partial", "complete"}
    )
    if value not in choices:
        _bad(f"Invalid stored {attribute} declaration.")
    return value


def project(item, element, attribute, selected="all"):
    if is_all(selected):
        if attribute == "n_" + element + "s":
            return count(item, element)
        if element == "atom" and attribute == "n_components":
            return count(item, "component")
        positions = list(range(count(item, element)))
    else:
        positions = _positions(item, element, selected)
    if positions is None:
        return None
    if attribute == element + "_index":
        return positions
    if attribute == "n_" + element + "s":
        return len(positions)
    state = _state(item)
    return project_arrays(
        element,
        attribute,
        positions,
        n_atoms=header(item)[1],
        n_components=_table(state, "components")[1],
        membership=lambda selected=None: _membership(item, state, selected),
        pairs=lambda: _pairs(item, state),
    )


def field(item, element, attribute, selected="all"):
    positions = None if is_all(selected) else _positions(item, element, selected)
    if positions is None and not is_all(selected):
        return None
    state = _state(item)

    def atom_has_column(name):
        table, rows = _table(state, "atom_attributes")
        if rows != header(item)[1]:
            _bad("Atom attribute rows do not match the chemical atom domain.")
        return name in table["columns"]

    return project_fields(
        element,
        attribute,
        positions,
        n_atoms=header(item)[1],
        n_bonds=_table(state, "bonds")[1],
        n_components=_table(state, "components")[1],
        atom_has_column=atom_has_column,
        column_values=lambda table, name, selected, size: _column(
            state, table, name, selected, size
        ),
        membership=lambda selected: _membership(item, state, selected),
    )


def has_attribute(item, attribute, include_none):
    data, atoms, size, reference = header(item)
    if include_none or attribute in {"n_atoms", "n_chemical_states"}:
        return True
    if attribute == "reference_chemical_state_index":
        return reference is not None
    if attribute == "chemical_state_index":
        return bool(size)
    if attribute == "chemical_state_id":
        return any(record.get("state_id") is not None for record in data["states"])
    if attribute == "atom_index":
        return bool(atoms)
    if not size:
        return False
    state = _state(item)
    if attribute == "bond_index":
        return bool(_table(state, "bonds")[1])
    if attribute == "component_index":
        return (
            bool(_table(state, "components")[1])
            or not _raw(state.get("component_indices"), atoms, {"Int64"})[1].all()
        )
    if (
        attribute in ATOM_FIELDS
        or attribute in BOND_FIELDS
        or attribute in COMPONENT_FIELDS
    ):
        table_name = (
            "atom_attributes"
            if attribute in ATOM_FIELDS
            else "bonds"
            if attribute in BOND_FIELDS
            else "components"
        )
        table, rows = _table(state, table_name)
        columns = (
            (ATOM_FIELDS[attribute],)
            if attribute in ATOM_FIELDS
            else BOND_FIELDS.get(attribute, (attribute,))
        )
        return any(
            name in table["columns"]
            and not _raw(table["columns"][name], rows, _expected(table_name, name))[
                1
            ].all()
            for name in columns
        )
    return True
