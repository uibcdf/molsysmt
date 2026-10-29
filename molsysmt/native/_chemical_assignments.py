"""Prepare typed assignments without publishing chemical state or owner changes."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.variables import is_all

from ._chemical_state import _BOND_OPTIONAL_DTYPES, Bonds_DataFrame, _coerce_bond_table


def assign_field(item, attribute, values, selected="all"):
    """Delegate one public atom/bond assignment to its selected chemical owner."""
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.smonitor import ArgumentError

    from ._chemical_fields import ATOM_FIELDS, BOND_FIELDS
    from ._chemical_queries import indices

    element = "atom" if attribute in ATOM_FIELDS else "bond"
    # Resolve even an empty selection: no edit may invent a missing state.
    item._resolve_chemical_state()
    positions = None if is_all(selected) else indices(item, element, selected)
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
