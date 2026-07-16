"""Translate ParmEd chemistry without confusing force terms with bond semantics."""

import math

import pandas as pd


_INTEGRAL_QUALITATIVE_ORDERS = {
    'ZERO': 0,
    'SINGLE': 1,
    'DOUBLE': 2,
    'TRIPLE': 3,
    'QUADRUPLE': 4,
    'QUINTUPLE': 5,
    'HEXTUPLE': 6,
}
_FRACTIONAL_QUALITATIVE_ORDERS = {
    'ONEANDAHALF': 1.5,
    'TWOANDAHALF': 2.5,
    'THREEANDAHALF': 3.5,
    'FOURANDAHALF': 4.5,
    'FIVEANDAHALF': 5.5,
}
_DATIVE_TYPES = {'DATIVEONE', 'DATIVE', 'DATIVEL', 'DATIVER'}
_UNSUPPORTED_RELATIONSHIPS = {'IONIC', 'HYDROGEN', 'THREECENTER', 'OTHER'}


def _qualitative_name(bond):
    qualitative_type = getattr(bond, 'qualitative_type', None)
    return None if qualitative_type is None else qualitative_type.name


def has_unsupported_relationships(structure):
    """Return whether ParmEd contains a relationship outside native bonds."""

    return any(
        _qualitative_name(bond) in _UNSUPPORTED_RELATIONSHIPS
        for bond in structure.bonds
    )


def has_mechanical_bond_types(structure):
    """Return whether any ParmEd bond carries force-field parameters."""

    return any(getattr(bond, 'type', None) is not None for bond in structure.bonds)


def bond_table_from_structure(structure):
    """Build canonical chemistry and report whether any relation was omitted."""

    rows = []
    omitted_relationship = False
    for bond in structure.bonds:
        qualitative_name = _qualitative_name(bond)
        if qualitative_name in _UNSUPPORTED_RELATIONSHIPS:
            omitted_relationship = True
            continue

        row = {
            'atom1_index': int(bond.atom1.idx),
            'atom2_index': int(bond.atom2.idx),
            'bond_type': 'covalent',
            'evidence': 'explicit',
        }

        order = getattr(bond, 'order', None)
        if order is not None:
            numeric_order = float(order)
            if math.isfinite(numeric_order) and numeric_order >= 0:
                if numeric_order.is_integer():
                    row['bond_order'] = int(numeric_order)
                else:
                    row['fractional_bond_order'] = numeric_order

        if qualitative_name in _INTEGRAL_QUALITATIVE_ORDERS:
            row['bond_order'] = _INTEGRAL_QUALITATIVE_ORDERS[qualitative_name]
        elif qualitative_name in _FRACTIONAL_QUALITATIVE_ORDERS:
            row['fractional_bond_order'] = _FRACTIONAL_QUALITATIVE_ORDERS[
                qualitative_name
            ]
        elif qualitative_name == 'AROMATIC':
            row['is_aromatic'] = True
        elif qualitative_name in _DATIVE_TYPES:
            row['bond_type'] = 'dative'

        rows.append(row)

    if rows:
        return pd.DataFrame(rows), omitted_relationship
    return (
        pd.DataFrame(columns=['atom1_index', 'atom2_index']),
        omitted_relationship,
    )
