"""Translate MDAnalysis bond metadata into the canonical chemical-state schema."""

import math

import pandas as pd


_ORDER_LABELS = {
    'single': 1,
    'double': 2,
    'triple': 3,
    'quadruple': 4,
}
_RECOGNIZED_TYPE_LABELS = set(_ORDER_LABELS) | {'aromatic', 'covalent', 'dative'}


def has_opaque_bond_types(topology):
    """Return whether independent scalar bond labels cannot be canonicalized."""

    if not hasattr(topology, 'bonds'):
        return False
    for value in getattr(topology.bonds, 'types', ()):
        if value is None or not isinstance(value, str):
            continue
        if value.strip().lower() not in _RECOGNIZED_TYPE_LABELS:
            return True
    return False


def _apply_value(row, value):
    """Apply one documented MDAnalysis order or type value to a bond row."""

    if value is None or value is pd.NA:
        return
    try:
        if pd.isna(value):
            return
    except (TypeError, ValueError):
        pass

    if isinstance(value, bool):
        return
    if isinstance(value, (int, float)):
        numeric_value = float(value)
        if not math.isfinite(numeric_value) or numeric_value < 0:
            return
        if numeric_value.is_integer():
            row['bond_order'] = int(numeric_value)
        else:
            row['fractional_bond_order'] = numeric_value
        return

    if not isinstance(value, str):
        return
    label = value.strip().lower()
    if label in _ORDER_LABELS:
        row['bond_order'] = _ORDER_LABELS[label]
    elif label == 'aromatic':
        row['is_aromatic'] = True
    elif label in {'covalent', 'dative'}:
        row['bond_type'] = label


def bond_table_from_topology(topology):
    """Build a canonical bond table from one MDAnalysis Topology."""

    if not hasattr(topology, 'bonds'):
        return pd.DataFrame(columns=['atom1_index', 'atom2_index'])

    bonds = topology.bonds
    values = list(bonds.values)
    types = list(getattr(bonds, 'types', [None] * len(values)))
    orders = list(getattr(bonds, 'order', [None] * len(values)))
    guessed = list(getattr(bonds, '_guessed', [False] * len(values)))

    rows = []
    for endpoints, type_value, order_value, is_guessed in zip(
        values, types, orders, guessed, strict=True
    ):
        row = {
            'atom1_index': int(endpoints[0]),
            'atom2_index': int(endpoints[1]),
            'bond_type': 'covalent',
            'evidence': 'inferred' if bool(is_guessed) else 'explicit',
        }
        _apply_value(row, order_value)
        _apply_value(row, type_value)
        rows.append(row)

    if rows:
        return pd.DataFrame(rows)
    return pd.DataFrame(columns=['atom1_index', 'atom2_index'])
