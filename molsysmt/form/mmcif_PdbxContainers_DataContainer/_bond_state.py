"""Normalize mmCIF connectivity into canonical chemical-state bond rows."""

from __future__ import annotations

import pandas as pd


_ORDER_CODES = {
    'SING': {'bond_order': 1},
    'DOUB': {'bond_order': 2},
    'TRIP': {'bond_order': 3},
    'QUAD': {'bond_order': 4},
    'AROM': {'is_aromatic': True},
    'DELO': {'is_conjugated': True},
}
_MERGED_FIELDS = (
    'bond_order',
    'fractional_bond_order',
    'bond_type',
    'is_aromatic',
    'is_conjugated',
    'evidence',
)


def metadata_from_chem_comp_bond(record, attributes):
    """Return canonical metadata supplied by one ``chem_comp_bond`` row."""

    metadata = {'bond_type': 'covalent', 'evidence': 'explicit'}
    if 'value_order' in attributes:
        value = str(record[attributes['value_order']]).strip().upper()
        metadata.update(_ORDER_CODES.get(value, {}))
    if 'pdbx_aromatic_flag' in attributes:
        value = str(record[attributes['pdbx_aromatic_flag']]).strip().upper()
        if value == 'Y':
            metadata['is_aromatic'] = True
    return metadata


def has_unknown_chem_comp_bond_orders(container):
    """Return whether supplied mmCIF order codes lack a canonical mapping."""

    if not container.exists('chem_comp_bond'):
        return False
    category = container.getObj('chem_comp_bond')
    attributes = {
        name: index for index, name in enumerate(category.getAttributeList())
    }
    if 'value_order' not in attributes:
        return False
    order_index = attributes['value_order']
    for record in category:
        value = str(record[order_index]).strip().upper()
        if value not in _ORDER_CODES and value not in {'', '.', '?'}:
            return True
    return False


class BondAccumulator:
    """Keep endpoints and metadata aligned while merging duplicate sources."""

    def __init__(self):
        self._rows = {}
        self.has_inference = False
        self.has_conflict = False

    @staticmethod
    def _key(endpoints):
        atom1, atom2 = sorted((int(endpoints[0]), int(endpoints[1])))
        return atom1, atom2

    def __contains__(self, endpoints):
        return self._key(endpoints) in self._rows

    def add(self, endpoints, **metadata):
        """Add or merge one canonical undirected bond."""

        key = self._key(endpoints)
        evidence = metadata.get('evidence', 'inferred')
        if evidence == 'inferred':
            self.has_inference = True
        incoming = {
            'atom1_index': key[0],
            'atom2_index': key[1],
            'bond_type': 'covalent',
            'evidence': evidence,
        }
        incoming.update(metadata)

        current = self._rows.get(key)
        if current is None:
            self._rows[key] = incoming
            return

        current_explicit = current.get('evidence') == 'explicit'
        incoming_explicit = incoming.get('evidence') == 'explicit'
        for field in _MERGED_FIELDS:
            old = current.get(field, pd.NA)
            new = incoming.get(field, pd.NA)
            old_missing = pd.isna(old)
            new_missing = pd.isna(new)
            if new_missing:
                continue
            if old_missing or (incoming_explicit and not current_explicit):
                current[field] = new
            elif old != new and incoming_explicit and current_explicit:
                current[field] = pd.NA
                self.has_conflict = True

        if current_explicit or incoming_explicit:
            current['evidence'] = 'explicit'

    def extend(self, endpoints, **metadata):
        """Add multiple bonds sharing the same metadata."""

        for pair in endpoints:
            self.add(pair, **metadata)

    def remap(self, kept_indices, replacements=None):
        """Remap complete records after alternate-location atom filtering."""

        replacements = replacements or {}
        index_map = {old: new for new, old in enumerate(kept_indices)}
        remapped = BondAccumulator()
        remapped.has_inference = self.has_inference
        remapped.has_conflict = self.has_conflict
        for row in self._rows.values():
            atom1 = replacements.get(row['atom1_index'], row['atom1_index'])
            atom2 = replacements.get(row['atom2_index'], row['atom2_index'])
            if atom1 not in index_map or atom2 not in index_map or atom1 == atom2:
                continue
            metadata = {
                key: value
                for key, value in row.items()
                if key not in {'atom1_index', 'atom2_index'}
            }
            remapped.add((index_map[atom1], index_map[atom2]), **metadata)
        remapped.has_inference |= self.has_inference
        remapped.has_conflict |= self.has_conflict
        return remapped

    @property
    def pairs(self):
        """Return sorted endpoint pairs."""

        return [list(pair) for pair in sorted(self._rows)]

    def to_dataframe(self):
        """Return sorted canonical rows without materializing absent columns."""

        rows = [self._rows[key] for key in sorted(self._rows)]
        if not rows:
            return pd.DataFrame(columns=['atom1_index', 'atom2_index'])
        return pd.DataFrame(rows)
