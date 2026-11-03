"""Prepare typed assignments without publishing chemical state or owner changes."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.variables import is_all

from ._chemical_state import _BOND_OPTIONAL_DTYPES, Bonds_DataFrame, _coerce_bond_table


def assignment_positions(item, element, selected, *, state=None):
    """Validate ordered unique write positions without enumerating a full axis."""
    from molsysmt._private.smonitor import ArgumentError

    from ._chemical_queries import indices

    positions = (
        None if is_all(selected) else indices(item, element, selected, state=state)
    )
    if positions is None and not is_all(selected):
        raise ArgumentError(
            "indices", value=selected, caller="molsysmt.ChemicalStates assignment"
        )
    if positions is not None and len(np.unique(positions)) != len(positions):
        raise ArgumentError(
            "indices",
            value=selected,
            caller="molsysmt.ChemicalStates assignment",
            message="Assignment positions must be unique; repeated writes are ambiguous.",
        )
    return positions


def assign_field(item, attribute, values, selected="all"):
    """Delegate one public atom/bond assignment to its selected chemical owner."""
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.smonitor import ArgumentError

    from ._chemical_fields import ATOM_FIELDS, BOND_FIELDS

    element = "atom" if attribute in ATOM_FIELDS else "bond"
    # Resolve even an empty selection: no edit may invent a missing state.
    item._resolve_chemical_state()
    positions = assignment_positions(item, element, selected)
    if element == "atom":
        if attribute == "formal_charge" and puw.is_quantity(values):
            values = puw.get_value(values, to_unit="elementary_charge")
            if not np.all(np.isfinite(values)):
                raise ArgumentError(
                    "formal_charge",
                    value=values,
                    caller="molsysmt.ChemicalStates assignment",
                    message="Formal-charge quantities must contain finite integer counts.",
                )
        item._set_chemical_state_atom_attribute(
            ATOM_FIELDS[attribute], values, atom_indices=positions
        )
    elif attribute == "bond_stereo_atom_indices":
        item._set_chemical_state_bond_stereo_atom_indices(
            values, bond_indices="all" if positions is None else positions
        )
    else:
        item._set_chemical_state_bond_attribute(
            BOND_FIELDS[attribute][0],
            values,
            bond_indices="all" if positions is None else positions,
        )


def _component_values(name, values):
    """Validate untrusted scalar/vector component data before typed staging."""
    from ._chemical_component_values import normalize_assignment

    normalized = normalize_assignment(
        name, values, caller="molsysmt.ChemicalStates assignment"
    )
    if name == "component_id" and isinstance(normalized, list):
        return [None if value is None else str(value) for value in normalized]
    return normalized


def _component_vector(name, values, size):
    """Broadcast a scalar/singleton or require an aligned component vector."""
    if values is None or isinstance(values, str):
        return [values] * size
    if len(values) == 1:
        return values * size
    if len(values) != size:
        raise StructuralInconsistencyError(
            reason=f"Component field {name!r} received {len(values)} values; expected {size}.",
            caller="molsysmt.native.ChemicalStates",
        )
    return values


def component_membership(item, state, values, positions):
    """Stage a partial declaration using only the state's existing component rows."""
    from ._chemical_components import unchanged_rows
    from ._chemical_state import Components_DataFrame

    size = item.n_atoms if positions is None else len(positions)
    if not size:
        return {}
    state._validate_atom_domain(item.n_atoms)
    values = _component_values("component_index", values)
    normalized = pd.array(
        _component_vector("component_index", values, size), dtype="Int64"
    )
    if np.any(
        normalized.to_numpy(dtype=np.int64, na_value=-1) >= len(state.components)
    ):
        raise StructuralInconsistencyError(
            reason="Declared component indices must refer to existing rows in the selected state.",
            caller="molsysmt.native.ChemicalStates",
        )
    candidate = state.component_indices.copy()
    if positions is None:
        candidate[:] = normalized
    else:
        candidate.iloc[positions] = normalized
    if candidate.equals(state.component_indices):
        return {}
    old = state.component_indices.to_numpy(dtype=np.int64, na_value=-1)
    new = candidate.to_numpy(dtype=np.int64, na_value=-1)
    count = len(state.components)
    new_rows, old_rows = unchanged_rows(old, new, count, count)
    components = Components_DataFrame(n_components=count)
    for column in components:
        components[column] = pd.array([pd.NA] * count, dtype="string")
        components.loc[new_rows, column] = (
            state.components[column].iloc[old_rows].to_numpy()
        )
    return {
        "component_indices": candidate,
        "components": components,
        "_component_completeness": "partial"
        if candidate.notna().any()
        else "unavailable",
        "_component_evidence": "user_defined",
    }


def component_labels(item, state, element, name, values, positions):
    """Stage component labels, rejecting conflicting atom-to-row projections."""
    from ._chemical_fields import COMPONENT_FIELDS
    from ._chemical_queries import _membership

    if name not in COMPONENT_FIELDS or element not in {"atom", "component"}:
        raise StructuralInconsistencyError(
            reason=f"Unsupported component label {name!r}.",
            caller="molsysmt.native.ChemicalStates",
        )
    size = (
        (item.n_atoms if element == "atom" else len(state.components))
        if positions is None
        else len(positions)
    )
    if not size:
        return None
    values = _component_values(name, values)
    if element == "atom":
        rows = _membership(item, state, positions)
        if np.any(rows < 0):
            raise StructuralInconsistencyError(
                reason="Selected atoms need known component membership before assigning a component label.",
                caller="molsysmt.native.ChemicalStates",
            )
    else:
        rows = (
            np.arange(size)
            if positions is None
            else np.asarray(positions, dtype=np.int64)
        )
    if values is None or isinstance(values, str) or len(values) == 1:
        rows = np.unique(rows)
        normalized = _component_vector(name, values, len(rows))
    else:
        normalized = _component_vector(name, values, size)
        by_row = {}
        for row, value in zip(rows, normalized):
            if row in by_row and value != by_row[row]:
                raise StructuralInconsistencyError(
                    reason="Selected atoms assign conflicting labels to the same component.",
                    caller="molsysmt.native.ChemicalStates",
                )
            by_row[row] = value
        rows = list(by_row)
        normalized = list(by_row.values())
    if name == "component_id":
        normalized = [None if value is None else str(value) for value in normalized]
    candidate = state.components.copy(deep=True)
    column = pd.array(state.components[name], dtype="string")
    column[rows] = pd.array(normalized, dtype="string")
    candidate[name] = column
    return candidate


def bond_selection(bond_indices, count):
    """Resolve positional rows without truncating floats or accepting booleans."""
    if is_all(bond_indices):
        return np.arange(count, dtype=np.int64)
    indices = np.atleast_1d(np.asarray(bond_indices))
    if indices.ndim != 1 or any(
        isinstance(value, (bool, np.bool_))
        for value in np.asarray(bond_indices, dtype=object).flat
    ):
        raise StructuralInconsistencyError(
            reason="Bond assignment indices must be a one-dimensional integer sequence.",
            caller="molsysmt.native.ChemicalStates",
        )
    if not indices.size:
        return np.empty(0, dtype=np.int64)
    if (
        not np.issubdtype(indices.dtype, np.integer)
        or np.any(indices < 0)
        or np.any(indices >= count)
    ):
        raise StructuralInconsistencyError(
            reason="Bond assignment indices are outside the selected state's bond domain.",
            caller="molsysmt.native.ChemicalStates",
        )
    return indices.astype(np.int64, copy=False)


def bond_attribute(bonds, name, values, indices, n_atoms):
    """Prepare a canonical bond column, retaining untouched rows and metadata."""
    if name not in _BOND_OPTIONAL_DTYPES:
        raise StructuralInconsistencyError(
            reason=f"Unsupported canonical bond attribute {name!r}.",
            caller="molsysmt.native.ChemicalStates",
        )
    indices = bond_selection(indices, len(bonds))
    if values is None or values is pd.NA or np.isscalar(values):
        normalized = [values] * len(indices)
    else:
        normalized = list(values)
        if len(normalized) != len(indices):
            raise StructuralInconsistencyError(
                reason=(
                    f"Bond attribute {name!r} received {len(normalized)} values; "
                    f"expected {len(indices)}."
                ),
                caller="molsysmt.native.ChemicalStates",
            )
    if not len(indices):
        return None
    if name == "bond_id":
        # Label edits must not infer participation flags, discard nullable
        # columns or reorder bond positions from a lossless decoded payload.
        candidate = Bonds_DataFrame(n_bonds=len(bonds))
        for column in bonds:
            candidate[column] = bonds[column].array.copy()
    else:
        candidate = bonds.copy()
    if name not in candidate:
        candidate[name] = pd.array(
            [pd.NA] * len(candidate), dtype=_BOND_OPTIONAL_DTYPES[name]
        )
    candidate.loc[indices, name] = pd.array(
        normalized, dtype=_BOND_OPTIONAL_DTYPES[name]
    )
    normalized = _coerce_bond_table(candidate, n_atoms=n_atoms)
    return candidate if name == "bond_id" else normalized


def stereo_atom_indices(bonds, values, indices, n_atoms):
    """Prepare both stereo references as one validated atomic assignment."""
    indices = bond_selection(indices, len(bonds))
    if not len(indices):
        return None
    if values is None or values is pd.NA:
        normalized = np.full((len(indices), 2), pd.NA, dtype=object)
    else:
        normalized = np.asarray(values, dtype=object)
        if len(indices) == 1 and normalized.shape == (2,):
            normalized = normalized.reshape(1, 2)
        if normalized.shape != (len(indices), 2):
            raise StructuralInconsistencyError(
                reason=f"bond_stereo_atom_indices must have shape ({len(indices)}, 2).",
                caller="molsysmt.native.ChemicalStates",
            )
    candidate = bonds.copy()
    for column, values in zip(
        ("stereo_atom1_index", "stereo_atom2_index"), normalized.T
    ):
        if column not in candidate:
            candidate[column] = pd.array([pd.NA] * len(candidate), dtype="Int64")
        candidate.loc[indices, column] = pd.array(values, dtype="Int64")
    return _coerce_bond_table(candidate, n_atoms=n_atoms)
