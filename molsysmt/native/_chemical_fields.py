"""Project declared state fields without interpreting or repairing chemistry."""

import numpy as np
import pandas as pd

from molsysmt._private.variables import is_all

from ._chemical_queries import _membership, indices

ATOM_FIELDS = {
    "formal_charge": "formal_charge",
    "atom_is_aromatic": "is_aromatic",
    "n_unpaired_electrons": "n_unpaired_electrons",
    "n_implicit_hydrogens": "n_implicit_hydrogens",
    "n_explicit_hydrogens": "n_explicit_hydrogens",
    "allows_implicit_hydrogens": "allows_implicit_hydrogens",
    "atom_stereochemistry": "stereochemistry",
}
BOND_FIELDS = {
    "bond_id": ("bond_id",),
    "bond_order": ("bond_order",),
    "fractional_bond_order": ("fractional_bond_order",),
    "bond_type": ("bond_type",),
    "bond_is_aromatic": ("is_aromatic",),
    "bond_is_conjugated": ("is_conjugated",),
    "bond_stereochemistry": ("stereochemistry",),
    "bond_stereo_atom_indices": ("stereo_atom1_index", "stereo_atom2_index"),
    "bond_donor_atom_index": ("donor_atom_index",),
    "bond_acceptor_atom_index": ("acceptor_atom_index",),
    "bond_joins_components": ("joins_components",),
    "bond_evidence": ("evidence",),
}
COMPONENT_FIELDS = ("component_id", "component_name", "component_type")


def has_field(state, attribute):
    """Check materialized nonmissing values, preserving false and zero."""
    if attribute in ATOM_FIELDS:
        return state.has_atom_attribute(ATOM_FIELDS[attribute])
    table = state.bonds if attribute in BOND_FIELDS else state.components
    columns = BOND_FIELDS.get(attribute, (attribute,))
    return any(column in table and table[column].notna().any() for column in columns)


def _column(table, name, positions, size):
    """Return detached Python scalars, retaining nulls and ordered repetitions."""
    if name not in table:
        return [None] * size
    values = table[name] if positions is None else table[name].iloc[positions]
    return [
        None
        if pd.isna(value)
        else value.item()
        if isinstance(value, np.generic)
        else value
        for value in values
    ]


def field(item, element, attribute, selected="all"):
    """Read only the selected column; absent atom properties stay unavailable."""
    # The all-axis case needs no Python list of every row position.
    positions = None if is_all(selected) else indices(item, element, selected)
    if positions is None and not is_all(selected):
        return None
    state = item._resolve_chemical_state()
    return project_fields(
        element,
        attribute,
        positions,
        n_atoms=item.n_atoms,
        n_bonds=len(state.bonds),
        n_components=len(state.components),
        atom_has_column=lambda name: name in state.atom_attributes,
        column_values=lambda table, name, selected, size: _column(
            getattr(state, table), name, selected, size
        ),
        membership=lambda selected: _membership(item, state, selected),
    )


def project_fields(
    element,
    attribute,
    positions,
    *,
    n_atoms,
    n_bonds,
    n_components,
    atom_has_column,
    column_values,
    membership,
):
    """Project nullable fields through native or typed-column read boundaries."""
    if attribute in ATOM_FIELDS:
        column = ATOM_FIELDS[attribute]
        if not atom_has_column(column):
            return None
        size = n_atoms if positions is None else len(positions)
        return column_values("atom_attributes", column, positions, size)
    if attribute in BOND_FIELDS:
        size = n_bonds if positions is None else len(positions)
        columns = [
            column_values("bonds", column, positions, size)
            for column in BOND_FIELDS[attribute]
        ]
        return columns[0] if len(columns) == 1 else [list(row) for row in zip(*columns)]
    if element == "atom":
        membership = membership(positions)
        # Mask unknown membership before indexing: -1 must never read the last row.
        known = membership >= 0
        output = [None] * len(membership)
        values = column_values(
            "components", attribute, membership[known], int(known.sum())
        )
        for position, value in zip(np.flatnonzero(known), values):
            output[position] = value
        return output
    size = n_components if positions is None else len(positions)
    return column_values("components", attribute, positions, size)
