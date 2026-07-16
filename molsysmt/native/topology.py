import pandas as pd
import numpy as np
from molsysmt._private.variables import is_all
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.lib.series import occurrence_order
import string
from contextlib import contextmanager
from contextvars import ContextVar
from smonitor import signal


_ACTIVE_CHEMICAL_STATE_INDICES = ContextVar(
    'molsysmt_active_chemical_state_indices', default={}
)

# Canonical schemas — these are fixed by design.
# To change them a conscious, explicit decision must be made and documented.
#
# Atoms: atom_id, atom_name, atom_type, isotope, group_index, chain_index
#   Component membership is atom-aligned but belongs to each chemical state;
#   chain_index remains part of the stable atom inventory.
#   A covalent drug–receptor adduct is TWO molecules but ONE component, which is
#   only expressible when component membership is atom-level, not group-level.
#
# Groups: group_id, group_name, group_type, molecule_index
#   Groups do NOT have component_index or chain_index. Component membership is
#   atom-aligned state data; chain membership belongs to stable atoms.

_ATOMS_COLUMNS  = frozenset(['atom_id', 'atom_name', 'atom_type', 'isotope',
                              'group_index', 'chain_index'])
_GROUPS_COLUMNS = frozenset(['group_id', 'group_name', 'group_type', 'molecule_index'])


class Atoms_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing atom-level topology fields.

    Schema (fixed): atom_id, atom_name, atom_type, isotope, group_index, chain_index.
    """

    def __init__(self, n_atoms=0):
        columns = ['atom_id', 'atom_name', 'atom_type', 'isotope', 'group_index', 'chain_index']
        super().__init__(index=range(n_atoms), columns=columns)
        self['atom_id'] = self['atom_id'].astype('string')
        self['atom_name'] = self['atom_name'].astype(str)
        self['atom_type'] = self['atom_type'].astype(str)
        self['isotope'] = self['isotope'].astype('UInt16')
        self['group_index'] = self['group_index'].astype('Int64')
        self['chain_index'] = self['chain_index'].astype('Int64')

    def __setitem__(self, key, value):
        if isinstance(key, str) and key not in _ATOMS_COLUMNS:
            raise AttributeError(
                f"Atoms_DataFrame has no column '{key}'. "
                f"Allowed columns: {sorted(_ATOMS_COLUMNS)}. "
                "To change the schema, update topology.py deliberately."
            )
        super().__setitem__(key, value)

    def _fix_null_values(self):
        for column in self:
            self[column] = self[column].fillna(pd.NA)
        self['atom_id'] = self['atom_id'].astype('string')
        self['isotope'] = self['isotope'].astype('UInt16')


class Groups_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing group-level topology fields.

    Schema (fixed): group_id, group_name, group_type, molecule_index.

    component_index and chain_index are NOT group-level attributes. Component
    membership is atom-aligned chemical-state data and chain membership lives
    on stable atoms. Writing either here raises AttributeError.
    """

    def __init__(self, n_groups=0):
        columns = ['group_id', 'group_name', 'group_type', 'molecule_index']
        super().__init__(index=range(n_groups), columns=columns)
        self['group_id'] = self['group_id'].astype('string')
        self['group_name'] = self['group_name'].astype(str)
        self['group_type'] = self['group_type'].astype(str)
        self['molecule_index'] = self['molecule_index'].astype('Int64')

    def __setitem__(self, key, value):
        if isinstance(key, str) and key not in _GROUPS_COLUMNS:
            raise AttributeError(
                f"Groups_DataFrame has no column '{key}'. "
                f"Allowed columns: {sorted(_GROUPS_COLUMNS)}. "
                "component_index is atom-aligned chemical-state data and "
                "chain_index belongs to atoms; neither belongs to groups. "
                "To change the schema, update topology.py deliberately."
            )
        super().__setitem__(key, value)

    def _fix_null_values(self):
        for column in self:
            self[column] = self[column].fillna(pd.NA)
        self['group_id'] = self['group_id'].astype('string')


class Molecules_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing molecule-level fields."""

    def __init__(self, n_molecules=0):
        """Initialize a molecules table with default types."""

        columns = ['molecule_id', 'molecule_name', 'molecule_type', 'entity_index']

        super().__init__(index=range(n_molecules), columns=columns)


        self['molecule_id'] = self['molecule_id'].astype('string')
        self['molecule_name'] = self['molecule_name'].astype(str)
        self['molecule_type'] = self['molecule_type'].astype(str)
        self['entity_index'] = self['entity_index'].astype('Int64')

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['molecule_id'] = self['molecule_id'].astype('string')


class Entities_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing entity-level fields."""

    def __init__(self, n_entities=0):
        """Initialize an entities table with default types."""

        columns = ['entity_id', 'entity_name', 'entity_type']

        super().__init__(index=range(n_entities), columns=columns)

        self['entity_id'] = self['entity_id'].astype('string')
        self['entity_name'] = self['entity_name'].astype(str)
        self['entity_type'] = self['entity_type'].astype(str)

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""


        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['entity_id'] = self['entity_id'].astype('string')


class Components_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing component-level fields."""

    def __init__(self, n_components=0):
        """Initialize a components table with default types."""

        columns = ['component_id', 'component_name', 'component_type']

        super().__init__(index=range(n_components), columns=columns)

        self['component_id'] = self['component_id'].astype('string')
        self['component_name'] = self['component_name'].astype(str)
        self['component_type'] = self['component_type'].astype(str)

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['component_id'] = self['component_id'].astype('string')


class Chains_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing chain-level fields."""

    def __init__(self, n_chains=0):
        """Initialize a chains table with default types."""

        columns = ['chain_id', 'chain_name', 'chain_type']

        super().__init__(index=range(n_chains), columns=columns)

        self['chain_id'] = self['chain_id'].astype('string')
        self['chain_name'] = self['chain_name'].astype(str)
        self['chain_type'] = self['chain_type'].astype(str)

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['chain_id'] = self['chain_id'].astype('string')


_BOND_REQUIRED_COLUMNS = ('atom1_index', 'atom2_index')
_BOND_OPTIONAL_DTYPES = {
    'bond_id': 'string',
    'bond_order': 'UInt8',
    'fractional_bond_order': 'Float64',
    'bond_type': 'string',
    'is_aromatic': 'boolean',
    'is_conjugated': 'boolean',
    'stereochemistry': 'string',
    'stereo_atom1_index': 'Int64',
    'stereo_atom2_index': 'Int64',
    'donor_atom_index': 'Int64',
    'acceptor_atom_index': 'Int64',
    'joins_components': 'boolean',
    'evidence': 'string',
    'provenance_index': 'Int64',
}
_BOND_ALLOWED_COLUMNS = frozenset(_BOND_REQUIRED_COLUMNS) | frozenset(_BOND_OPTIONAL_DTYPES)
_BOND_ATOM_REFERENCE_COLUMNS = (
    'atom1_index', 'atom2_index', 'stereo_atom1_index', 'stereo_atom2_index',
    'donor_atom_index', 'acceptor_atom_index',
)


class Bonds_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing normalized chemical-state bonds."""

    def __init__(self, n_bonds=0):
        """Initialize a bonds table with default types."""

        super().__init__(index=range(n_bonds), columns=list(_BOND_REQUIRED_COLUMNS))

        self['atom1_index'] = self['atom1_index'].astype('Int64')
        self['atom2_index'] = self['atom2_index'].astype('Int64')

    def __setitem__(self, key, value):
        if isinstance(key, str) and key not in _BOND_ALLOWED_COLUMNS:
            raise AttributeError(
                f"Bonds_DataFrame has no canonical column {key!r}. "
                f"Allowed columns: {sorted(_BOND_ALLOWED_COLUMNS)}."
            )
        super().__setitem__(key, value)
        if isinstance(key, str):
            dtype = 'Int64' if key in _BOND_REQUIRED_COLUMNS else _BOND_OPTIONAL_DTYPES[key]
            super().__setitem__(key, pd.array(self[key], dtype=dtype))

    def _reset(self, n_bonds=0):
        """Rebuild the bonds table to a clean state with the given size."""

        super().__init__(index=range(n_bonds), columns=list(_BOND_REQUIRED_COLUMNS))

        self['atom1_index'] = self['atom1_index'].astype('Int64')
        self['atom2_index'] = self['atom2_index'].astype('Int64')

    def _fix_null_values(self):
        """Normalize missing values in optional bond columns."""

        self['atom1_index'] = pd.array(self['atom1_index'], dtype='Int64')
        self['atom2_index'] = pd.array(self['atom2_index'], dtype='Int64')
        for column, dtype in _BOND_OPTIONAL_DTYPES.items():
            if column in self.columns:
                self[column] = pd.array(self[column], dtype=dtype)

    def _sort_bonds(self):
        """Sort bonds so `atom1_index` is always <= `atom2_index`."""

        mask = self['atom1_index'] > self['atom2_index']
        self.loc[mask, ['atom1_index', 'atom2_index']] = self.loc[mask, ['atom2_index', 'atom1_index']].values
        self.sort_values(by=['atom1_index', 'atom2_index'], inplace=True)
        self.reset_index(drop=True, inplace=True)

    def _remove_empty_columns(self):
        """Drop optional columns when they only contain NaN placeholders."""

        for column in _BOND_OPTIONAL_DTYPES:
            if column in self.columns:
                if self[column].isna().all():
                    del self[column]


_CHEMICAL_STATE_COMPLETENESS_VALUES = frozenset({'unavailable', 'partial', 'complete'})
_CHEMICAL_STATE_EVIDENCE_VALUES = frozenset({'explicit', 'inferred', 'user_defined', 'unknown'})
_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES = {
    'formal_charge': 'Int16',
    'is_aromatic': 'boolean',
    'n_unpaired_electrons': 'UInt8',
    'n_implicit_hydrogens': 'UInt8',
    'allows_implicit_hydrogens': 'boolean',
    'stereochemistry': 'string',
}
_CHEMICAL_STATE_ATOM_STEREOCHEMISTRY_VALUES = frozenset(
    {'R', 'S', 'r', 's', 'unspecified', 'unknown'}
)


class _ChemicalStateStorage:
    """Store the private data owned by one chemical state.

    Optional atom-state columns are materialized only when assigned. Component
    membership is an always-aligned nullable vector because it is the link to
    the state-local component table, not stable topology inventory.
    """

    def __init__(self, n_atoms=0, bonds=None, components=None, component_indices=None, state_id=None,
                 connectivity_completeness='unavailable', component_completeness='unavailable',
                 component_evidence='unknown', provenance_index=None):
        self.state_id = None if state_id is None else str(state_id)
        self.atom_attributes = pd.DataFrame(index=range(n_atoms))
        if component_indices is None:
            component_indices = [pd.NA] * n_atoms
        self.component_indices = pd.Series(
            pd.array(component_indices, dtype='Int64'), index=range(n_atoms)
        )
        self.bonds = Bonds_DataFrame(n_bonds=0) if bonds is None else bonds
        self.components = Components_DataFrame(n_components=0) if components is None else components
        self.connectivity_completeness = connectivity_completeness
        self.component_completeness = component_completeness
        self.component_evidence = component_evidence
        self.provenance_index = provenance_index

    @staticmethod
    def _validate_choice(field, value, choices):
        if value not in choices:
            raise StructuralInconsistencyError(
                reason=f"Invalid chemical-state {field} {value!r}; expected one of {sorted(choices)}.",
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )
        return value

    @property
    def connectivity_completeness(self):
        return self._connectivity_completeness

    @connectivity_completeness.setter
    def connectivity_completeness(self, value):
        self._connectivity_completeness = self._validate_choice(
            'connectivity completeness', value, _CHEMICAL_STATE_COMPLETENESS_VALUES
        )

    @property
    def component_completeness(self):
        return self._component_completeness

    @component_completeness.setter
    def component_completeness(self, value):
        self._component_completeness = self._validate_choice(
            'component completeness', value, _CHEMICAL_STATE_COMPLETENESS_VALUES
        )

    @property
    def component_evidence(self):
        return self._component_evidence

    @component_evidence.setter
    def component_evidence(self, value):
        self._component_evidence = self._validate_choice(
            'component evidence', value, _CHEMICAL_STATE_EVIDENCE_VALUES
        )

    @property
    def provenance_index(self):
        return self._provenance_index

    @provenance_index.setter
    def provenance_index(self, value):
        if value is not None:
            if not isinstance(value, (int, np.integer)) or value < 0:
                raise StructuralInconsistencyError(
                    reason='Chemical-state provenance_index must be a non-negative integer or None.',
                    caller='molsysmt.native.topology._ChemicalStateStorage',
                )
            value = int(value)
        self._provenance_index = value

    def _ensure_compatibility(self, n_atoms):
        """Fill metadata absent from storage created by an older MolSysMT."""

        if not hasattr(self, 'state_id'):
            self.state_id = None
        if not hasattr(self, 'atom_attributes'):
            self.atom_attributes = pd.DataFrame(index=range(n_atoms))
        if len(self.atom_attributes.index) != n_atoms:
            if self.atom_attributes.shape[1] == 0:
                self.atom_attributes = pd.DataFrame(index=range(n_atoms))
            else:
                raise StructuralInconsistencyError(
                    reason=(
                        'Chemical-state atom attributes are not aligned with the stable atom inventory: '
                        f'{len(self.atom_attributes.index)} rows for {n_atoms} atoms.'
                    ),
                    caller='molsysmt.native.topology._ChemicalStateStorage',
                )
        if not hasattr(self, 'component_indices'):
            self.component_indices = pd.Series(
                pd.array([pd.NA] * n_atoms, dtype='Int64'), index=range(n_atoms)
            )
        elif len(self.component_indices.index) != n_atoms:
            if self.component_indices.isna().all():
                self.component_indices = pd.Series(
                    pd.array([pd.NA] * n_atoms, dtype='Int64'), index=range(n_atoms)
                )
            else:
                raise StructuralInconsistencyError(
                    reason=(
                        'Chemical-state component membership is not aligned with the stable atom inventory: '
                        f'{len(self.component_indices.index)} rows for {n_atoms} atoms.'
                    ),
                    caller='molsysmt.native.topology._ChemicalStateStorage',
                )
        else:
            self.component_indices = pd.Series(
                pd.array(self.component_indices, dtype='Int64'), index=range(n_atoms)
            )
        if not hasattr(self, '_connectivity_completeness'):
            self._connectivity_completeness = 'unavailable'
        if not hasattr(self, '_component_completeness'):
            self._component_completeness = 'unavailable'
        if not hasattr(self, '_component_evidence'):
            self._component_evidence = 'unknown'
        if not hasattr(self, '_provenance_index'):
            self._provenance_index = None

        self._normalize_atom_attribute_columns()

    def _normalize_atom_attribute_columns(self):
        """Validate names, order, and nullable dtypes of atom-state columns."""

        unknown_columns = set(self.atom_attributes.columns) - set(_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES)
        if unknown_columns:
            raise StructuralInconsistencyError(
                reason=f'Unknown chemical-state atom attributes: {sorted(unknown_columns)}.',
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )
        ordered_columns = [
            name for name in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES if name in self.atom_attributes.columns
        ]
        self.atom_attributes = self.atom_attributes.reindex(columns=ordered_columns)
        for name in ordered_columns:
            self.atom_attributes[name] = self._coerce_atom_attribute(name, self.atom_attributes[name])

    @staticmethod
    def _coerce_atom_attribute(name, values):
        """Return one validated nullable array for an atom-state attribute."""

        if name not in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES:
            raise StructuralInconsistencyError(
                reason=f'Unknown chemical-state atom attribute {name!r}.',
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )

        values = list(values)
        non_missing = [value for value in values if not pd.isna(value)]

        if name == 'stereochemistry':
            invalid = sorted({str(value) for value in non_missing} - _CHEMICAL_STATE_ATOM_STEREOCHEMISTRY_VALUES)
            if invalid:
                raise StructuralInconsistencyError(
                    reason=(
                        f'Invalid atom stereochemistry values {invalid}; expected values from '
                        f'{sorted(_CHEMICAL_STATE_ATOM_STEREOCHEMISTRY_VALUES)}.'
                    ),
                    caller='molsysmt.native.topology._ChemicalStateStorage',
                )

        if _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name] == 'boolean':
            invalid = [value for value in non_missing if not isinstance(value, (bool, np.bool_))]
            if invalid:
                raise StructuralInconsistencyError(
                    reason=f'Chemical-state atom attribute {name!r} accepts only boolean or missing values.',
                    caller='molsysmt.native.topology._ChemicalStateStorage',
                )

        try:
            return pd.array(values, dtype=_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name])
        except (TypeError, ValueError, OverflowError) as error:
            raise StructuralInconsistencyError(
                reason=(
                    f'Values for chemical-state atom attribute {name!r} cannot be represented as '
                    f'{_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name]}: {error}'
                ),
                caller='molsysmt.native.topology._ChemicalStateStorage',
            ) from error

    def _normalize_atom_indices(self, atom_indices):
        """Return validated atom indices for a partial atom-state operation."""

        indices = np.asarray(atom_indices)
        if indices.ndim != 1 or not np.issubdtype(indices.dtype, np.integer):
            raise StructuralInconsistencyError(
                reason='Chemical-state atom indices must be a one-dimensional integer sequence.',
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )
        indices = indices.astype(np.int64, copy=False)
        if len(np.unique(indices)) != len(indices):
            raise StructuralInconsistencyError(
                reason='Chemical-state atom indices must not contain duplicates.',
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )
        if np.any(indices < 0) or np.any(indices >= len(self.atom_attributes.index)):
            raise StructuralInconsistencyError(
                reason=(
                    f'Chemical-state atom indices are outside the valid range '
                    f'[0, {len(self.atom_attributes.index)}).'
                ),
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )
        return indices

    @staticmethod
    def _values_with_length(values, expected_length, name):
        """Broadcast a scalar or validate a sequence length."""

        if values is None or values is pd.NA or np.isscalar(values):
            return [values] * expected_length
        values = list(values)
        if len(values) != expected_length:
            raise StructuralInconsistencyError(
                reason=(
                    f'Chemical-state atom attribute {name!r} received {len(values)} values; '
                    f'expected {expected_length}.'
                ),
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )
        return values

    def has_atom_attribute(self, name, include_none=False):
        """Return whether this state contains a meaningful atom-state column."""

        if name not in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES:
            return False
        if name not in self.atom_attributes.columns:
            return False
        return include_none or not self.atom_attributes[name].isna().all()

    def get_atom_attribute(self, name, atom_indices=None):
        """Return an optional atom-state series or a validated subset."""

        if name not in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES:
            raise StructuralInconsistencyError(
                reason=f'Unknown chemical-state atom attribute {name!r}.',
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )
        if name not in self.atom_attributes.columns:
            return None
        if atom_indices is None:
            return self.atom_attributes[name]
        indices = self._normalize_atom_indices(atom_indices)
        return self.atom_attributes[name].iloc[indices]

    def set_atom_attribute(self, name, values, atom_indices=None):
        """Set a complete or partial optional atom-state column."""

        if name not in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES:
            raise StructuralInconsistencyError(
                reason=f'Unknown chemical-state atom attribute {name!r}.',
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )
        if atom_indices is None:
            normalized_values = self._values_with_length(values, len(self.atom_attributes.index), name)
            self.atom_attributes[name] = self._coerce_atom_attribute(name, normalized_values)
        else:
            indices = self._normalize_atom_indices(atom_indices)
            normalized_values = self._values_with_length(values, len(indices), name)
            if name not in self.atom_attributes.columns:
                self.atom_attributes[name] = pd.array(
                    [pd.NA] * len(self.atom_attributes.index),
                    dtype=_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name],
                )
            coerced_values = self._coerce_atom_attribute(name, normalized_values)
            self.atom_attributes.loc[indices, name] = coerced_values
            self.atom_attributes[name] = self._coerce_atom_attribute(name, self.atom_attributes[name])
        self._normalize_atom_attribute_columns()

    def remove_atom_attribute(self, name):
        """Remove an optional atom-state column if it is materialized."""

        if name not in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES:
            raise StructuralInconsistencyError(
                reason=f'Unknown chemical-state atom attribute {name!r}.',
                caller='molsysmt.native.topology._ChemicalStateStorage',
            )
        if name in self.atom_attributes.columns:
            self.atom_attributes.drop(columns=name, inplace=True)

    def copy(self):
        """Return an independent copy of this private chemical state."""

        output = _ChemicalStateStorage(
            n_atoms=len(self.atom_attributes.index),
            bonds=self.bonds.copy(),
            components=self.components.copy(),
            component_indices=self.component_indices.copy(deep=True),
            state_id=self.state_id,
            connectivity_completeness=self.connectivity_completeness,
            component_completeness=self.component_completeness,
            component_evidence=self.component_evidence,
            provenance_index=self.provenance_index,
        )
        output.atom_attributes = self.atom_attributes.copy(deep=True)
        return output


# Keeping the old private class name allows pickles produced during the staged
# migration to resolve their original class reference.
_ReferenceChemicalStateStorage = _ChemicalStateStorage

class Topology():
    """Native topology container including atoms, groups, chains, and bonds."""

    @arg_digest()
    def __init__(self, n_atoms=0, n_groups=0, n_components=0, n_molecules=0, n_entities=0, n_chains=0, n_bonds=0,
                skip_digestion=False):
        """Initialize empty topology tables with the requested sizes."""

        self._chemical_states = [_ChemicalStateStorage(n_atoms=n_atoms)]
        self._reference_chemical_state_index = 0
        self.reset_atoms(n_atoms=n_atoms)
        self.reset_groups(n_groups=n_groups)
        self.reset_components(n_components=n_components)
        self.reset_molecules(n_molecules=n_molecules)
        self.reset_entities(n_entities=n_entities)
        self.reset_chains(n_chains=n_chains)
        self.reset_bonds(n_bonds=n_bonds)
        self._coerce_id_columns_to_string()

        # Dirty bits for hierarchy reconstruction
        self._atoms_dirty = False
        self._groups_dirty = False
        self._components_dirty = False
        self._molecules_dirty = False
        self._entities_dirty = False
        self._chains_dirty = False

    @property
    def _reference_chemical_state(self):
        """Return the resolved private reference chemical state."""

        return self._resolve_reference_chemical_state()

    @_reference_chemical_state.setter
    def _reference_chemical_state(self, value):
        """Restore or replace the resolved private reference state."""

        if not hasattr(self, '_chemical_states') or len(self._chemical_states) == 0:
            self._chemical_states = [value]
            self._reference_chemical_state_index = 0
            return
        state_index = self._resolve_reference_chemical_state_index()
        self._chemical_states[state_index] = value

    def _resolve_reference_chemical_state_index(self):
        """Resolve the private reference-state index without guessing."""

        n_states = len(self._chemical_states)
        if n_states == 0:
            raise StructuralInconsistencyError(
                reason='Topology has no chemical state; state-dependent data are unavailable.',
                caller='molsysmt.native.Topology',
            )
        if n_states == 1:
            return 0
        state_index = self._reference_chemical_state_index
        if state_index is None:
            raise StructuralInconsistencyError(
                reason=(
                    f'Topology has {n_states} chemical states and no reference state; '
                    'state-dependent access is ambiguous.'
                ),
                caller='molsysmt.native.Topology',
            )
        if not isinstance(state_index, (int, np.integer)) or not 0 <= int(state_index) < n_states:
            raise StructuralInconsistencyError(
                reason=f'Reference chemical-state index {state_index!r} is invalid for {n_states} states.',
                caller='molsysmt.native.Topology',
            )
        return int(state_index)

    def _resolve_reference_chemical_state(self):
        """Return the private state selected by the reference-state rules."""

        return self._chemical_states[self._resolve_reference_chemical_state_index()]

    def _resolve_chemical_state(self, state_index=None):
        """Return an explicitly indexed state or the resolved reference state."""

        if state_index is None:
            state_index = _ACTIVE_CHEMICAL_STATE_INDICES.get().get(id(self))
            if state_index is None:
                return self._resolve_reference_chemical_state()
        if isinstance(state_index, (bool, np.bool_)) or not isinstance(
            state_index, (int, np.integer)
        ):
            raise StructuralInconsistencyError(
                reason='Chemical-state index must be an integer or None.',
                caller='molsysmt.native.Topology',
            )
        state_index = int(state_index)
        if not 0 <= state_index < len(self._chemical_states):
            raise StructuralInconsistencyError(
                reason=f'Chemical-state index {state_index} is invalid for {len(self._chemical_states)} states.',
                caller='molsysmt.native.Topology',
            )
        return self._chemical_states[state_index]

    def _chemical_state_inventory_equals(self, item):
        """Return whether stable atoms and ordered chemical states match exactly."""

        if not isinstance(item, Topology):
            return False
        for table_name in ('atoms', 'groups', 'molecules', 'entities', 'chains'):
            if not getattr(self, table_name).equals(getattr(item, table_name)):
                return False
        if self._reference_chemical_state_index != item._reference_chemical_state_index:
            return False
        if len(self._chemical_states) != len(item._chemical_states):
            return False
        metadata = (
            'state_id',
            'connectivity_completeness',
            'component_completeness',
            'component_evidence',
            'provenance_index',
        )
        for left, right in zip(self._chemical_states, item._chemical_states):
            if any(getattr(left, name) != getattr(right, name) for name in metadata):
                return False
            if not left.component_indices.equals(right.component_indices):
                return False
            if not left.components.equals(right.components):
                return False
            if not left.atom_attributes.equals(right.atom_attributes):
                return False
            if not left.bonds.equals(right.bonds):
                return False
        return True

    @contextmanager
    def _using_chemical_state(self, state_index):
        """Resolve state-dependent facades against one state within this context."""

        self._resolve_chemical_state(state_index=state_index)
        active_indices = _ACTIVE_CHEMICAL_STATE_INDICES.get()
        token = _ACTIVE_CHEMICAL_STATE_INDICES.set(
            {**active_indices, id(self): int(state_index)}
        )
        try:
            yield self
        finally:
            _ACTIVE_CHEMICAL_STATE_INDICES.reset(token)

    def _has_chemical_state_atom_attribute(self, name, state_index=None, include_none=False):
        """Return private instance availability for an atom-state attribute."""

        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        return state.has_atom_attribute(name, include_none=include_none)

    def _get_chemical_state_atom_attribute(self, name, atom_indices=None, state_index=None):
        """Return one private atom-state attribute from a resolved state."""

        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        return state.get_atom_attribute(name, atom_indices=atom_indices)

    def _set_chemical_state_atom_attribute(self, name, values, atom_indices=None, state_index=None):
        """Set one private atom-state attribute on a resolved state."""

        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        state.set_atom_attribute(name, values, atom_indices=atom_indices)

    def _remove_chemical_state_atom_attribute(self, name, state_index=None):
        """Remove one private optional atom-state attribute."""

        state = self._resolve_chemical_state(state_index=state_index)
        state.remove_atom_attribute(name)

    @staticmethod
    def _coerce_bond_table(value, n_atoms=None):
        """Normalize canonical or legacy bond storage into the v1 schema."""

        if not isinstance(value, pd.DataFrame):
            raise StructuralInconsistencyError(
                reason='Chemical-state bonds must be provided as a Pandas DataFrame.',
                caller='molsysmt.native.Topology',
            )

        required_columns = {'atom1_index', 'atom2_index'}
        missing_columns = required_columns - set(value.columns)
        if missing_columns:
            raise StructuralInconsistencyError(
                reason=f'Chemical-state bond table is missing required columns: {sorted(missing_columns)}.',
                caller='molsysmt.native.Topology',
            )

        unexpected_columns = set(value.columns) - _BOND_ALLOWED_COLUMNS - {'order', 'type'}
        if unexpected_columns:
            raise StructuralInconsistencyError(
                reason=f'Chemical-state bond table has unsupported columns: {sorted(unexpected_columns)}.',
                caller='molsysmt.native.Topology',
            )

        output = Bonds_DataFrame(n_bonds=value.shape[0])
        try:
            output['atom1_index'] = pd.array(value['atom1_index'], dtype='Int64')
            output['atom2_index'] = pd.array(value['atom2_index'], dtype='Int64')
        except (TypeError, ValueError, OverflowError) as error:
            raise StructuralInconsistencyError(
                reason=f'Bond endpoint indices must be integers: {error}',
                caller='molsysmt.native.Topology',
            ) from error

        if output[list(_BOND_REQUIRED_COLUMNS)].isna().any(axis=None):
            raise StructuralInconsistencyError(
                reason='Bond endpoint indices must not be missing.',
                caller='molsysmt.native.Topology',
            )

        atom1 = output['atom1_index'].to_numpy(dtype=np.int64)
        atom2 = output['atom2_index'].to_numpy(dtype=np.int64)
        if np.any(atom1 == atom2):
            raise StructuralInconsistencyError(
                reason='Self-bonds are not valid chemical-state edges.',
                caller='molsysmt.native.Topology',
            )
        if n_atoms is not None and (
            np.any(atom1 < 0) or np.any(atom2 < 0)
            or np.any(atom1 >= n_atoms) or np.any(atom2 >= n_atoms)
        ):
            raise StructuralInconsistencyError(
                reason=f'Bond endpoint indices must be between 0 and {n_atoms - 1}.',
                caller='molsysmt.native.Topology',
            )

        swap = atom1 > atom2
        if np.any(swap):
            atom1[swap], atom2[swap] = atom2[swap].copy(), atom1[swap].copy()
            output['atom1_index'] = pd.array(atom1, dtype='Int64')
            output['atom2_index'] = pd.array(atom2, dtype='Int64')
        if len(set(zip(atom1.tolist(), atom2.tolist()))) != len(atom1):
            raise StructuralInconsistencyError(
                reason='Only one bond is allowed per unordered atom pair.',
                caller='molsysmt.native.Topology',
            )

        for column, dtype in _BOND_OPTIONAL_DTYPES.items():
            if column in value.columns:
                try:
                    output[column] = pd.array(value[column], dtype=dtype)
                except (TypeError, ValueError, OverflowError) as error:
                    raise StructuralInconsistencyError(
                        reason=f'Invalid values for bond field {column!r}: {error}',
                        caller='molsysmt.native.Topology',
                    ) from error

        def _missing(raw_value):
            if raw_value is None or raw_value is pd.NA:
                return True
            try:
                return bool(pd.isna(raw_value))
            except (TypeError, ValueError):
                return False

        def _set_value(row_index, column, normalized_value):
            if normalized_value is None:
                return
            if column not in output.columns:
                output[column] = pd.array(
                    [pd.NA] * len(output.index), dtype=_BOND_OPTIONAL_DTYPES[column]
                )
            current = output.at[row_index, column]
            if not _missing(current) and current != normalized_value:
                raise StructuralInconsistencyError(
                    reason=(
                        f'Conflicting legacy and canonical bond values for {column!r} '
                        f'at row {row_index}.'
                    ),
                    caller='molsysmt.native.Topology',
                )
            try:
                output.at[row_index, column] = normalized_value
            except (TypeError, ValueError, OverflowError) as error:
                raise StructuralInconsistencyError(
                    reason=(
                        f'Legacy bond value {normalized_value!r} cannot be represented '
                        f'in canonical field {column!r}: {error}'
                    ),
                    caller='molsysmt.native.Topology',
                ) from error

        order_aliases = {'single': 1, 'double': 2, 'triple': 3, 'quadruple': 4}

        def _normalize_legacy_label(raw_value, field, row_index):
            if _missing(raw_value):
                return
            if isinstance(raw_value, (bool, np.bool_)):
                raise StructuralInconsistencyError(
                    reason=f'Boolean values are not valid legacy bond {field}.',
                    caller='molsysmt.native.Topology',
                )
            if isinstance(raw_value, (int, float, np.integer, np.floating)):
                numeric_value = float(raw_value)
                if not np.isfinite(numeric_value) or numeric_value < 0:
                    raise StructuralInconsistencyError(
                        reason=f'Invalid legacy bond {field} value {raw_value!r}.',
                        caller='molsysmt.native.Topology',
                    )
                if numeric_value.is_integer():
                    _set_value(row_index, 'bond_order', int(numeric_value))
                else:
                    _set_value(row_index, 'fractional_bond_order', numeric_value)
                return

            label = str(raw_value).strip().lower()
            if label in {'', 'none', '<na>', 'nan', 'unspecified'}:
                return
            if label in order_aliases:
                _set_value(row_index, 'bond_order', order_aliases[label])
                return
            if label == 'aromatic':
                _set_value(row_index, 'is_aromatic', True)
                return
            if label in {'covalent', 'dative', 'unknown'}:
                _set_value(row_index, 'bond_type', label)
                return
            try:
                numeric_value = float(label)
            except ValueError as error:
                raise StructuralInconsistencyError(
                    reason=(
                        f'Legacy bond {field} value {raw_value!r} has no unambiguous '
                        'mapping to the normalized chemical schema.'
                    ),
                    caller='molsysmt.native.Topology',
                ) from error
            _normalize_legacy_label(numeric_value, field, row_index)

        for legacy_column in ('order', 'type'):
            if legacy_column in value.columns:
                for row_index, raw_value in enumerate(value[legacy_column].tolist()):
                    _normalize_legacy_label(raw_value, legacy_column, row_index)

        if 'bond_type' in output.columns:
            allowed_bond_types = {'covalent', 'dative', 'unknown'}
            invalid = set(output['bond_type'].dropna().tolist()) - allowed_bond_types
            if invalid:
                raise StructuralInconsistencyError(
                    reason=f'Invalid canonical bond_type values: {sorted(invalid)}.',
                    caller='molsysmt.native.Topology',
                )
            if 'joins_components' not in output.columns:
                output['joins_components'] = pd.array(
                    [pd.NA] * len(output.index), dtype='boolean'
                )
            covalent = output['bond_type'].eq('covalent').fillna(False)
            dative = output['bond_type'].eq('dative').fillna(False)
            explicit_override = (
                (covalent & output['joins_components'].eq(False).fillna(False))
                | (dative & output['joins_components'].eq(True).fillna(False))
            )
            if explicit_override.any():
                if 'evidence' not in output.columns or output.loc[
                    explicit_override, 'evidence'
                ].isna().any():
                    raise StructuralInconsistencyError(
                        reason=(
                            'A non-default joins_components value requires explicit '
                            'bond evidence.'
                        ),
                        caller='molsysmt.native.Topology',
                    )
            output.loc[covalent & output['joins_components'].isna(), 'joins_components'] = True
            output.loc[dative & output['joins_components'].isna(), 'joins_components'] = False

        if 'joins_components' in output.columns:
            lacks_default = output['joins_components'].notna()
            if 'bond_type' in output.columns:
                lacks_default &= ~output['bond_type'].isin(['covalent', 'dative'])
            if lacks_default.any() and (
                'evidence' not in output.columns
                or output.loc[lacks_default, 'evidence'].isna().any()
            ):
                raise StructuralInconsistencyError(
                    reason=(
                        'joins_components without a covalent or dative default '
                        'requires explicit bond evidence.'
                    ),
                    caller='molsysmt.native.Topology',
                )

        if 'evidence' in output.columns:
            invalid = set(output['evidence'].dropna().tolist()) - _CHEMICAL_STATE_EVIDENCE_VALUES
            if invalid:
                raise StructuralInconsistencyError(
                    reason=f'Invalid bond evidence values: {sorted(invalid)}.',
                    caller='molsysmt.native.Topology',
                )

        if 'fractional_bond_order' in output.columns:
            fractional_orders = output['fractional_bond_order'].dropna().to_numpy(dtype=float)
            if np.any(~np.isfinite(fractional_orders)) or np.any(fractional_orders < 0):
                raise StructuralInconsistencyError(
                    reason='Fractional bond order must be finite and non-negative.',
                    caller='molsysmt.native.Topology',
                )
        if 'provenance_index' in output.columns:
            provenance_indices = output['provenance_index'].dropna().to_numpy(dtype=np.int64)
            if np.any(provenance_indices < 0):
                raise StructuralInconsistencyError(
                    reason='Bond provenance indices must be non-negative.',
                    caller='molsysmt.native.Topology',
                )

        for column in (
            'stereo_atom1_index', 'stereo_atom2_index', 'donor_atom_index',
            'acceptor_atom_index',
        ):
            if column in output.columns and n_atoms is not None:
                indices = output[column].dropna().to_numpy(dtype=np.int64)
                if np.any(indices < 0) or np.any(indices >= n_atoms):
                    raise StructuralInconsistencyError(
                        reason=f'Bond field {column!r} contains atom indices outside the topology.',
                        caller='molsysmt.native.Topology',
                    )

        for column in ('donor_atom_index', 'acceptor_atom_index'):
            if column in output.columns:
                invalid_reference = output[column].notna() & ~(
                    output[column].eq(output['atom1_index'])
                    | output[column].eq(output['atom2_index'])
                )
                if invalid_reference.any():
                    raise StructuralInconsistencyError(
                        reason=f'Bond field {column!r} must reference one of the bond endpoints.',
                        caller='molsysmt.native.Topology',
                    )
        if {'donor_atom_index', 'acceptor_atom_index'} <= set(output.columns):
            same_directional_endpoint = (
                output['donor_atom_index'].notna()
                & output['acceptor_atom_index'].notna()
                & output['donor_atom_index'].eq(output['acceptor_atom_index'])
            )
            if same_directional_endpoint.any():
                raise StructuralInconsistencyError(
                    reason='Bond donor and acceptor atom indices must be distinct.',
                    caller='molsysmt.native.Topology',
                )

        if 'stereochemistry' in output.columns:
            has_stereochemistry = output['stereochemistry'].notna()
            missing_references = pd.Series(False, index=output.index)
            for column in ('stereo_atom1_index', 'stereo_atom2_index'):
                if column not in output.columns:
                    missing_references |= has_stereochemistry
                else:
                    missing_references |= has_stereochemistry & output[column].isna()
            if missing_references.any():
                raise StructuralInconsistencyError(
                    reason='Bond stereochemistry requires two stereo reference atom indices.',
                    caller='molsysmt.native.Topology',
                )

        output._fix_null_values()
        output._remove_empty_columns()
        output._sort_bonds()
        return output

    @classmethod
    def _concatenate_bond_tables(cls, *tables):
        """Concatenate bond storage without all-missing optional dtype drift."""

        required_columns = {'atom1_index', 'atom2_index'}
        prepared = []
        for table in tables:
            keep_columns = [
                column
                for column in table.columns
                if column in required_columns or table[column].notna().any()
            ]
            prepared.append(table.loc[:, keep_columns])
        return cls._coerce_bond_table(
            pd.concat(prepared, ignore_index=True, copy=False)
        )

    @staticmethod
    def _remap_bond_atom_indices(table, index_map):
        """Return a bond table with every atom reference remapped together."""

        output = table.copy()
        for column in _BOND_ATOM_REFERENCE_COLUMNS:
            if column in output.columns:
                original = output[column]
                remapped = original.map(index_map)
                if column in {'atom1_index', 'atom2_index'} and remapped.isna().any():
                    raise StructuralInconsistencyError(
                        reason='Bond endpoints cannot be retained when their atoms are absent.',
                        caller='molsysmt.native.Topology',
                    )
                output[column] = pd.array(remapped, dtype='Int64')

        stereo_columns = {'stereo_atom1_index', 'stereo_atom2_index'} & set(output.columns)
        if stereo_columns:
            incomplete_stereo = output[list(stereo_columns)].isna().any(axis=1)
            for column in ('stereo_atom1_index', 'stereo_atom2_index', 'stereochemistry'):
                if column in output.columns:
                    output.loc[incomplete_stereo, column] = pd.NA
        return output

    def _get_chemical_state_bonds(self, state_index=None):
        """Return the single authoritative bond table for a resolved state."""

        return self._resolve_chemical_state(state_index=state_index).bonds

    def _set_chemical_state_bond_attribute(
        self, name, values, bond_indices='all', state_index=None
    ):
        """Set one normalized bond field on all or selected bonds atomically."""

        if name not in _BOND_OPTIONAL_DTYPES:
            raise StructuralInconsistencyError(
                reason=f'Unsupported canonical bond attribute {name!r}.',
                caller='molsysmt.native.Topology',
            )
        bonds = self._get_chemical_state_bonds(state_index=state_index).copy()
        if is_all(bond_indices):
            indices = np.arange(len(bonds), dtype=np.int64)
        else:
            indices = np.asarray(bond_indices, dtype=np.int64)
            if indices.ndim != 1 or np.any(indices < 0) or np.any(indices >= len(bonds)):
                raise StructuralInconsistencyError(
                    reason='Bond indices for chemical-state assignment are out of range.',
                    caller='molsysmt.native.Topology',
                )

        if values is None or values is pd.NA or np.isscalar(values):
            normalized = [values] * len(indices)
        else:
            normalized = list(values)
            if len(normalized) != len(indices):
                raise StructuralInconsistencyError(
                    reason=(
                        f'Bond attribute {name!r} received {len(normalized)} values; '
                        f'expected {len(indices)}.'
                    ),
                    caller='molsysmt.native.Topology',
                )

        if name not in bonds.columns:
            bonds[name] = pd.array(
                [pd.NA] * len(bonds), dtype=_BOND_OPTIONAL_DTYPES[name]
            )
        bonds.loc[indices, name] = pd.array(
            normalized, dtype=_BOND_OPTIONAL_DTYPES[name]
        )
        self._set_chemical_state_bonds(bonds, state_index=state_index)

    def _set_chemical_state_bond_stereo_atom_indices(
        self, values, bond_indices='all', state_index=None
    ):
        """Set the two stereo-reference atom indices as one public attribute."""

        bonds = self._get_chemical_state_bonds(state_index=state_index).copy()
        if is_all(bond_indices):
            indices = np.arange(len(bonds), dtype=np.int64)
        else:
            indices = np.asarray(bond_indices, dtype=np.int64)
            if indices.ndim != 1 or np.any(indices < 0) or np.any(indices >= len(bonds)):
                raise StructuralInconsistencyError(
                    reason='Bond indices for stereo-reference assignment are out of range.',
                    caller='molsysmt.native.Topology',
                )

        if values is None or values is pd.NA:
            normalized = [[pd.NA, pd.NA] for _ in indices]
        else:
            normalized = np.asarray(values, dtype=object)
            if normalized.ndim == 1 and len(indices) == 1 and normalized.shape == (2,):
                normalized = normalized.reshape(1, 2)
            if normalized.shape != (len(indices), 2):
                raise StructuralInconsistencyError(
                    reason=(
                        'bond_stereo_atom_indices must have shape '
                        f'({len(indices)}, 2).'
                    ),
                    caller='molsysmt.native.Topology',
                )

        for column, column_values in zip(
            ('stereo_atom1_index', 'stereo_atom2_index'), np.asarray(normalized).T
        ):
            if column not in bonds.columns:
                bonds[column] = pd.array([pd.NA] * len(bonds), dtype='Int64')
            bonds.loc[indices, column] = pd.array(column_values, dtype='Int64')
        self._set_chemical_state_bonds(bonds, state_index=state_index)

    def _set_chemical_state_bonds(self, value, state_index=None):
        """Replace the authoritative bond table without reinterpreting metadata."""

        if state_index is None:
            state = self._ensure_state_for_mutation()
        else:
            state = self._resolve_chemical_state(state_index=state_index)
        state.bonds = self._coerce_bond_table(value, n_atoms=self.n_atoms)
        if state.bonds.shape[0] and state.connectivity_completeness == 'unavailable':
            state.connectivity_completeness = 'partial'

    def _reset_chemical_state_bonds(self, n_bonds=0, state_index=None):
        """Reset one state's bond table, allowing explicit construction rows."""

        if state_index is None:
            state = self._ensure_state_for_mutation()
        else:
            state = self._resolve_chemical_state(state_index=state_index)
        state.bonds = Bonds_DataFrame(n_bonds=n_bonds)

    def _append_chemical_state_bonds(
        self, bonded_atom_pairs, orders=None, types=None, state_index=None,
        sort=True, **metadata
    ):
        """Append normalized or explicitly translated legacy bond rows."""

        bonded_atom_pairs = np.asarray(bonded_atom_pairs)
        if bonded_atom_pairs.size == 0:
            bonded_atom_pairs = np.empty((0, 2), dtype=int)
        if bonded_atom_pairs.ndim != 2 or bonded_atom_pairs.shape[1] != 2:
            raise StructuralInconsistencyError(
                reason='Bonded atom pairs must have shape (n_bonds, 2).',
                caller='molsysmt.native.Topology',
            )
        try:
            bonded_atom_pairs = bonded_atom_pairs.astype(int, copy=False)
        except (TypeError, ValueError, OverflowError) as error:
            raise StructuralInconsistencyError(
                reason=f'Bonded atom indices must be integers: {error}',
                caller='molsysmt.native.Topology',
            )

        if bonded_atom_pairs.size:
            if np.any(bonded_atom_pairs < 0) or np.any(bonded_atom_pairs >= self.n_atoms):
                raise StructuralInconsistencyError(
                    reason=f'Bonded atom indices must be between 0 and {self.n_atoms - 1}.',
                    caller='molsysmt.native.Topology',
                )

        n_new_bonds = bonded_atom_pairs.shape[0]

        def _metadata_values(values, field):
            if values is None:
                return [pd.NA] * n_new_bonds
            if np.isscalar(values) or values is pd.NA:
                return [values] * n_new_bonds
            values = list(values)
            if len(values) != n_new_bonds:
                raise StructuralInconsistencyError(
                    reason=f'Bond {field} received {len(values)} values; expected {n_new_bonds}.',
                    caller='molsysmt.native.Topology',
                )
            return values

        unexpected_metadata = set(metadata) - set(_BOND_OPTIONAL_DTYPES)
        if unexpected_metadata:
            raise StructuralInconsistencyError(
                reason=f'Unsupported bond metadata fields: {sorted(unexpected_metadata)}.',
                caller='molsysmt.native.Topology',
            )

        new_bonds = pd.DataFrame({
            'atom1_index': bonded_atom_pairs[:, 0],
            'atom2_index': bonded_atom_pairs[:, 1],
        })
        if orders is not None:
            new_bonds['order'] = _metadata_values(orders, 'order')
        if types is not None:
            new_bonds['type'] = _metadata_values(types, 'type')
        for field, values in metadata.items():
            new_bonds[field] = _metadata_values(values, field)
        new_bonds = self._coerce_bond_table(new_bonds, n_atoms=self.n_atoms)

        if state_index is None:
            state = self._ensure_state_for_mutation()
            current_bonds = state.bonds
        else:
            state = self._resolve_chemical_state(state_index=state_index)
            current_bonds = state.bonds
        combined = self._concatenate_bond_tables(current_bonds, new_bonds)
        combined = self._coerce_bond_table(combined, n_atoms=self.n_atoms)
        if not sort:
            combined.reset_index(drop=True, inplace=True)
        self._set_chemical_state_bonds(combined, state_index=state_index)
        if n_new_bonds and state.connectivity_completeness == 'unavailable':
            state.connectivity_completeness = 'partial'

    def _remove_chemical_state_bonds(self, bond_indices='all', state_index=None):
        """Remove bond rows from a resolved state through the storage seam."""

        bonds = self._get_chemical_state_bonds(state_index=state_index)
        if is_all(bond_indices):
            self._reset_chemical_state_bonds(n_bonds=0, state_index=state_index)
            return
        bonds.drop(bond_indices, inplace=True)
        bonds.reset_index(drop=True, inplace=True)

    def _append_chemical_state(self, state_id=None, set_as_reference=False):
        """Append an empty private chemical state and return its index."""

        state = _ChemicalStateStorage(n_atoms=self.n_atoms, state_id=state_id)
        self._chemical_states.append(state)
        state_index = len(self._chemical_states) - 1
        if len(self._chemical_states) == 1 or set_as_reference:
            self._reference_chemical_state_index = state_index
        return state_index

    def _clear_chemical_states(self):
        """Remove all private chemical states without changing stable topology."""

        self._chemical_states = []
        self._reference_chemical_state_index = None

    def _set_reference_chemical_state_index(self, state_index):
        """Set the private reference-state index after validating it."""

        if state_index is None:
            self._reference_chemical_state_index = None
            return
        if isinstance(state_index, (bool, np.bool_)) or not isinstance(
            state_index, (int, np.integer)
        ):
            raise StructuralInconsistencyError(
                reason='Reference chemical-state index must be an integer or None.',
                caller='molsysmt.native.Topology',
            )
        state_index = int(state_index)
        if not 0 <= state_index < len(self._chemical_states):
            raise StructuralInconsistencyError(
                reason=(
                    f'Reference chemical-state index {state_index} is invalid for '
                    f'{len(self._chemical_states)} states.'
                ),
                caller='molsysmt.native.Topology',
            )
        self._reference_chemical_state_index = state_index

    def _ensure_state_for_mutation(self):
        """Return a reference state, creating one only for an explicit mutation."""

        if len(self._chemical_states) == 0:
            self._append_chemical_state(set_as_reference=True)
        return self._resolve_chemical_state()

    @property
    def bonds(self):
        """Return the bond table owned by the reference chemical state."""

        return self._get_chemical_state_bonds()

    @bonds.setter
    def bonds(self, value):
        """Replace the bond table owned by the reference chemical state."""

        self._set_chemical_state_bonds(value)

    @property
    def components(self):
        """Return the component table owned by the currently resolved chemical state."""

        return self._resolve_chemical_state().components

    @components.setter
    def components(self, value):
        """Replace the component table owned by the currently resolved chemical state."""

        self._ensure_state_for_mutation().components = value

    def __setstate__(self, state):
        """Restore topology state, migrating legacy direct table storage."""

        if 'atoms_dataframe' in state:
            self._restore_legacy_flat_state(state)
            return

        legacy_component_indices = None
        legacy_atoms = state.get('atoms')
        if legacy_atoms is not None and 'component_index' in legacy_atoms.columns:
            legacy_component_indices = legacy_atoms['component_index'].copy()
            legacy_atoms = legacy_atoms.drop(columns='component_index')
            state['atoms'] = legacy_atoms

        legacy_bonds = state.pop('bonds', None)
        legacy_components = state.pop('components', None)
        legacy_reference_state = state.pop('_reference_chemical_state', None)
        self.__dict__.update(state)
        if 'isotope' not in self.atoms.columns:
            self.atoms.insert(
                3, 'isotope', pd.array([pd.NA] * self.n_atoms, dtype='UInt16')
            )

        if '_chemical_states' not in self.__dict__:
            if legacy_reference_state is None:
                legacy_reference_state = _ChemicalStateStorage(
                    n_atoms=self.n_atoms,
                    bonds=legacy_bonds,
                    components=legacy_components,
                )
            self._chemical_states = [legacy_reference_state]
            self._reference_chemical_state_index = 0

        for chemical_state in self._chemical_states:
            chemical_state._ensure_compatibility(self.n_atoms)
            chemical_state.bonds = self._coerce_bond_table(
                chemical_state.bonds, n_atoms=self.n_atoms
            )

        if '_reference_chemical_state_index' not in self.__dict__:
            self._reference_chemical_state_index = 0 if len(self._chemical_states) == 1 else None

        if legacy_component_indices is not None and len(self._chemical_states):
            reference_index = self._resolve_reference_chemical_state_index()
            reference_state = self._chemical_states[reference_index]
            if reference_state.component_indices.isna().all():
                reference_state.component_indices = pd.Series(
                    pd.array(legacy_component_indices, dtype='Int64'), index=range(self.n_atoms)
                )

        if legacy_bonds is not None:
            self._set_chemical_state_bonds(legacy_bonds)
        if legacy_components is not None:
            self._ensure_state_for_mutation().components = legacy_components

    def _restore_legacy_flat_state(self, state):
        """Restore the pre-normalization flat atom and bond tables."""

        legacy_atoms = state['atoms_dataframe'].copy()
        legacy_bonds = state.get('bonds_dataframe')
        n_atoms = legacy_atoms.shape[0]

        def index_map(column):
            if column not in legacy_atoms:
                return {}
            output = {}
            for value in legacy_atoms[column]:
                if pd.notna(value) and value not in output:
                    output[value] = len(output)
            return output

        maps = {
            element: index_map(f'{element}_index')
            for element in ('group', 'component', 'molecule', 'entity', 'chain')
        }
        restored = type(self)(
            n_atoms=n_atoms,
            n_groups=len(maps['group']),
            n_components=len(maps['component']),
            n_molecules=len(maps['molecule']),
            n_entities=len(maps['entity']),
            n_chains=len(maps['chain']),
            skip_digestion=True,
        )
        self.__dict__.update(restored.__dict__)

        def values(column, default=None):
            if column in legacy_atoms:
                return legacy_atoms[column].tolist()
            return [default] * n_atoms

        self.atoms['atom_id'] = values('atom_id')
        self.atoms['atom_name'] = values('atom_name')
        self.atoms['atom_type'] = values('atom_type')
        self.atoms['isotope'] = pd.array(values('isotope'), dtype='UInt16')
        for element in ('group', 'component', 'chain'):
            column = f'{element}_index'
            mapped = [
                maps[element].get(value, pd.NA) if pd.notna(value) else pd.NA
                for value in values(column)
            ]
            if element == 'component':
                self._set_component_indices(mapped)
            else:
                self.atoms[column] = mapped

        def fill_table(element, table, columns):
            source_index = f'{element}_index'
            for old_index, new_index in maps[element].items():
                row = legacy_atoms.loc[legacy_atoms[source_index] == old_index].iloc[0]
                for target_column, source_column in columns.items():
                    if source_column in legacy_atoms:
                        value = row[source_column]
                        if target_column.endswith('_id') and pd.notna(value):
                            value = str(value)
                        table.loc[new_index, target_column] = value

        fill_table('component', self.components, {
            'component_id': 'component_id',
            'component_name': 'component_name',
            'component_type': 'component_type',
        })
        fill_table('entity', self.entities, {
            'entity_id': 'entity_id',
            'entity_name': 'entity_name',
            'entity_type': 'entity_type',
        })
        fill_table('chain', self.chains, {
            'chain_id': 'chain_id',
            'chain_name': 'chain_name',
            'chain_type': 'chain_type',
        })
        fill_table('molecule', self.molecules, {
            'molecule_id': 'molecule_id',
            'molecule_name': 'molecule_name',
            'molecule_type': 'molecule_type',
        })
        fill_table('group', self.groups, {
            'group_id': 'group_id',
            'group_name': 'group_name',
            'group_type': 'group_type',
        })

        for old_index, new_index in maps['group'].items():
            row = legacy_atoms.loc[legacy_atoms['group_index'] == old_index].iloc[0]
            molecule_index = row.get('molecule_index', pd.NA)
            self.groups.loc[new_index, 'molecule_index'] = maps['molecule'].get(
                molecule_index, pd.NA
            )
        for old_index, new_index in maps['molecule'].items():
            row = legacy_atoms.loc[legacy_atoms['molecule_index'] == old_index].iloc[0]
            entity_index = row.get('entity_index', pd.NA)
            self.molecules.loc[new_index, 'entity_index'] = maps['entity'].get(
                entity_index, pd.NA
            )

        if legacy_bonds is not None:
            atom_labels = values('atom_index')
            if len(set(atom_labels)) != n_atoms:
                raise StructuralInconsistencyError(
                    reason='Legacy serialized atom indices are not unique.',
                    caller='molsysmt.native.Topology.__setstate__',
                )
            atom_map = {label: index for index, label in enumerate(atom_labels)}
            migrated_bonds = legacy_bonds.copy()
            for endpoint in ('atom1_index', 'atom2_index'):
                migrated_bonds[endpoint] = [
                    atom_map[value] for value in migrated_bonds[endpoint]
                ]
            self._set_chemical_state_bonds(migrated_bonds)
            self._get_chemical_state_bonds()._sort_bonds()
            self._reference_chemical_state.connectivity_completeness = 'partial'

        component_values = values('component_index')
        if component_values and all(pd.notna(value) for value in component_values):
            self._reference_chemical_state.component_completeness = 'complete'
        self._reference_chemical_state.component_evidence = 'unknown'

        if 'formal_charge' in legacy_atoms and legacy_atoms['formal_charge'].notna().any():
            self._set_chemical_state_atom_attribute(
                'formal_charge',
                pd.array(legacy_atoms['formal_charge'], dtype='Int16'),
            )
        if 'partial_charge' in legacy_atoms and legacy_atoms['partial_charge'].notna().any():
            self._legacy_partial_charge = legacy_atoms['partial_charge'].to_numpy(copy=True)

        self._coerce_id_columns_to_string()

    def _get_component_indices(self, state_index=None):
        """Return authoritative component membership for a resolved state."""

        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        return state.component_indices

    def _set_component_indices(self, values, atom_indices=None, state_index=None):
        """Set authoritative component membership for a resolved state."""

        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        if atom_indices is None:
            normalized = _ChemicalStateStorage._values_with_length(
                values, self.n_atoms, 'component_index'
            )
            normalized = pd.array(normalized, dtype='Int64')
            if (pd.Series(normalized).dropna() < 0).any():
                raise StructuralInconsistencyError(
                    reason='Chemical-state component indices must be non-negative or missing.',
                    caller='molsysmt.native.Topology',
                )
            state.component_indices = pd.Series(normalized, index=range(self.n_atoms))
        else:
            indices = state._normalize_atom_indices(np.atleast_1d(atom_indices))
            normalized = _ChemicalStateStorage._values_with_length(
                values, len(indices), 'component_index'
            )
            normalized = pd.array(normalized, dtype='Int64')
            if (pd.Series(normalized).dropna() < 0).any():
                raise StructuralInconsistencyError(
                    reason='Chemical-state component indices must be non-negative or missing.',
                    caller='molsysmt.native.Topology',
                )
            state.component_indices.loc[indices] = normalized
            state.component_indices = pd.Series(
                pd.array(state.component_indices, dtype='Int64'), index=range(self.n_atoms)
            )

    def _component_indices_are_missing(self, state_index=None):
        """Return whether any resolved-state component membership is unknown."""

        return self._get_component_indices(state_index=state_index).isnull().any()

    def get_n_atoms(self):
        return self.atoms.shape[0]

    def get_n_groups(self):
        return self.groups.shape[0]

    def get_n_components(self):
        return self.components.shape[0]

    def get_n_molecules(self):
        return self.molecules.shape[0]

    def get_n_entities(self):
        return self.entities.shape[0]

    def get_n_chains(self):
        return self.chains.shape[0]

    def get_n_bonds(self):
        return self._get_chemical_state_bonds().shape[0]

    def reset_atoms(self, n_atoms=0):
        """Reset atoms table to a new size."""

        self.atoms = Atoms_DataFrame(n_atoms=n_atoms)

    def reset_groups(self, n_groups=0):
        """Reset groups table to a new size."""

        self.groups = Groups_DataFrame(n_groups=n_groups)

    def reset_components(self, n_components=0):
        """Reset components table to a new size."""

        self.components = Components_DataFrame(n_components=n_components)

    def reset_molecules(self, n_molecules=0):
        """Reset molecules table to a new size."""

        self.molecules = Molecules_DataFrame(n_molecules=n_molecules)

    def reset_entities(self, n_entities=0):
        """Reset entities table to a new size."""

        self.entities = Entities_DataFrame(n_entities=n_entities)

    def reset_chains(self, n_chains=0):
        """Reset chains table to a new size."""

        self.chains = Chains_DataFrame(n_chains=n_chains)

    def reset_bonds(self, n_bonds=0):
        """Reset bonds table to a new size."""

        self._reset_chemical_state_bonds(n_bonds=n_bonds)

    def _coerce_id_columns_to_string(self):
        """Ensure all *_id columns use pandas string dtype."""

        self.atoms['atom_id'] = self.atoms['atom_id'].astype('string')
        self.groups['group_id'] = self.groups['group_id'].astype('string')
        self.components['component_id'] = self.components['component_id'].astype('string')
        self.molecules['molecule_id'] = self.molecules['molecule_id'].astype('string')
        self.entities['entity_id'] = self.entities['entity_id'].astype('string')
        self.chains['chain_id'] = self.chains['chain_id'].astype('string')

    @property
    def n_atoms(self):
        return self.atoms.shape[0]

    @property
    def n_groups(self):
        return self.groups.shape[0]

    @property
    def n_components(self):
        return self.components.shape[0]

    @property
    def n_molecules(self):
        return self.molecules.shape[0]

    @property
    def n_entities(self):
        return self.entities.shape[0]

    @property
    def n_chains(self):
        return self.chains.shape[0]

    @property
    def n_bonds(self):
        return self._get_chemical_state_bonds().shape[0]

    @signal(tags=['native'])
    @arg_digest()
    def extract(self, atom_indices='all', copy_if_all=False, skip_digestion=False):
        """Return a subset topology with the selected atoms and associated hierarchy."""

        if is_all(atom_indices):

            if copy_if_all:
                return self.copy()
            else:
                return self

        elif len(atom_indices) == self.atoms.shape[0]:

            if copy_if_all:
                return self.copy()
            else:
                return self

        else:

            atom_indices = np.sort(atom_indices)

            tmp_item = Topology(skip_digestion=True)
            tmp_item.atoms = self.atoms.iloc[atom_indices].copy()
            tmp_item.atoms.reset_index(drop=True, inplace=True)

            old_group_indices = tmp_item.atoms['group_index'].dropna().unique().tolist()
            tmp_item.groups = self.groups.iloc[old_group_indices].copy()
            tmp_item.groups.reset_index(drop=True, inplace=True)

            old_molecule_indices = tmp_item.groups['molecule_index'].dropna().unique().tolist()
            tmp_item.molecules = self.molecules.iloc[old_molecule_indices].copy()
            tmp_item.molecules.reset_index(drop=True, inplace=True)

            old_entity_indices = tmp_item.molecules['entity_index'].dropna().unique().tolist()
            tmp_item.entities = self.entities.iloc[old_entity_indices].copy()
            tmp_item.entities.reset_index(drop=True, inplace=True)

            old_chain_indices = tmp_item.atoms['chain_index'].dropna().unique().tolist()
            tmp_item.chains = self.chains.iloc[old_chain_indices].copy()
            tmp_item.chains.reset_index(drop=True, inplace=True)

            tmp_item.atoms['group_index'] = tmp_item.atoms['group_index'].map({old: new for new, old in enumerate(old_group_indices)}).astype('Int64')
            tmp_item.groups['molecule_index'] = tmp_item.groups['molecule_index'].map({old: new for new, old in enumerate(old_molecule_indices)}).astype('Int64')
            tmp_item.molecules['entity_index'] = tmp_item.molecules['entity_index'].map({old: new for new, old in enumerate(old_entity_indices)}).astype('Int64')
            tmp_item.atoms['chain_index'] = tmp_item.atoms['chain_index'].map({old: new for new, old in enumerate(old_chain_indices)}).astype('Int64')

            atom_index_map = {old: new for new, old in enumerate(atom_indices)}
            extracted_states = []
            for source_state in self._chemical_states:
                source_state._ensure_compatibility(self.n_atoms)
                source_membership = source_state.component_indices.iloc[atom_indices].copy()
                old_component_indices = source_membership.dropna().unique().tolist()
                component_index_map = {
                    old: new for new, old in enumerate(old_component_indices)
                }
                extracted_components = source_state.components.iloc[old_component_indices].copy()
                extracted_components.reset_index(drop=True, inplace=True)
                extracted_membership = source_membership.map(component_index_map).astype('Int64')
                extracted_membership.reset_index(drop=True, inplace=True)

                source_bonds = source_state.bonds
                mask_atom1 = np.isin(source_bonds['atom1_index'], atom_indices)
                mask_atom2 = np.isin(source_bonds['atom2_index'], atom_indices)
                mask = mask_atom1 & mask_atom2
                extracted_bonds = source_bonds[mask].copy()
                extracted_bonds.reset_index(drop=True, inplace=True)
                extracted_bonds = self._remap_bond_atom_indices(
                    extracted_bonds, atom_index_map
                )
                extracted_state = _ChemicalStateStorage(
                    n_atoms=len(atom_indices),
                    bonds=self._coerce_bond_table(extracted_bonds, n_atoms=len(atom_indices)),
                    components=extracted_components,
                    component_indices=extracted_membership,
                    state_id=source_state.state_id,
                    connectivity_completeness=source_state.connectivity_completeness,
                    component_completeness=source_state.component_completeness,
                    component_evidence=source_state.component_evidence,
                    provenance_index=source_state.provenance_index,
                )
                extracted_state.atom_attributes = source_state.atom_attributes.iloc[atom_indices].copy()
                extracted_state.atom_attributes.reset_index(drop=True, inplace=True)
                extracted_state._normalize_atom_attribute_columns()
                extracted_states.append(extracted_state)

            tmp_item._chemical_states = extracted_states
            tmp_item._reference_chemical_state_index = self._reference_chemical_state_index
            tmp_item.atoms['atom_id'] = tmp_item.atoms['atom_id'].astype('string')
            tmp_item.groups['group_id'] = tmp_item.groups['group_id'].astype('string')
            tmp_item.molecules['molecule_id'] = tmp_item.molecules['molecule_id'].astype('string')
            tmp_item.entities['entity_id'] = tmp_item.entities['entity_id'].astype('string')
            tmp_item.chains['chain_id'] = tmp_item.chains['chain_id'].astype('string')
            for chemical_state in tmp_item._chemical_states:
                chemical_state.components['component_id'] = chemical_state.components['component_id'].astype('string')
            return tmp_item

    @signal(tags=['native'])
    @arg_digest()
    def remove(self, atom_indices=None, copy_if_None=False, skip_digestion=False):
        """Remove atoms by index and return the resulting topology."""

        if atom_indices is None:

            if copy_if_None:
                return self.copy()
            else:
                return self

        else:

            atom_indices_to_be_kept = np.setdiff1d(np.arange(self.n_atoms), atom_indices)

            tmp_item = self.extract(atom_indices=atom_indices_to_be_kept, skip_digestion=True)

            return tmp_item


    @signal(tags=['native'])
    @arg_digest(form='molsysmt.Topology')
    def add(self, item, atom_indices='all', keep_ids=True, skip_digestion=False):
        """Append another topology, offsetting indices as needed."""

        if len(self._chemical_states) != 1 or len(item._chemical_states) != 1:
            raise StructuralInconsistencyError(
                reason=(
                    'Adding topologies with multiple or absent chemical states requires an explicit '
                    'state-alignment policy and is not inferred automatically.'
                ),
                caller='molsysmt.native.Topology.add',
            )

        if is_all(atom_indices):
            tmp_item = item.copy()
        else:
            tmp_item = item.extract(atom_indices=atom_indices, skip_digestion=True)

        n_atoms = self.atoms.shape[0]
        n_groups = self.groups.shape[0]
        n_components = self.components.shape[0]
        n_molecules = self.molecules.shape[0]
        n_chains = self.chains.shape[0]

        tmp_item.atoms['group_index'] += n_groups
        tmp_item._set_component_indices(tmp_item._get_component_indices() + n_components)
        tmp_item.atoms['chain_index'] += n_chains
        tmp_item.groups['molecule_index'] += n_molecules
        combined_component_indices = pd.concat(
            [self._get_component_indices(), tmp_item._get_component_indices()],
            ignore_index=True,
        ).astype('Int64')
        combined_atom_attributes = pd.concat(
            [
                self._reference_chemical_state.atom_attributes,
                tmp_item._reference_chemical_state.atom_attributes,
            ],
            ignore_index=True,
        )
        tmp_bonds = tmp_item._get_chemical_state_bonds()
        if tmp_bonds.shape[0]:
            tmp_bonds = self._remap_bond_atom_indices(
                tmp_bonds, {index: index + n_atoms for index in range(tmp_item.n_atoms)}
            )

        self.atoms = pd.concat([self.atoms, tmp_item.atoms], ignore_index=True, copy=False)
        self._reference_chemical_state.component_indices = combined_component_indices
        self._reference_chemical_state.atom_attributes = combined_atom_attributes
        self._reference_chemical_state._normalize_atom_attribute_columns()
        self.groups = pd.concat([self.groups, tmp_item.groups], ignore_index=True, copy=False)
        self.molecules = pd.concat([self.molecules, tmp_item.molecules], ignore_index=True, copy=False)
        self.components = pd.concat([self.components, tmp_item.components], ignore_index=True, copy=False)
        self.chains = pd.concat([self.chains, tmp_item.chains], ignore_index=True, copy=False)
        combined_bonds = self._concatenate_bond_tables(
            self._get_chemical_state_bonds(), tmp_bonds
        )
        self._set_chemical_state_bonds(combined_bonds)

        if not keep_ids:
            self.rebuild_atoms(redefine_ids=True, redefine_types=False)
            self.rebuild_groups(redefine_ids=True, redefine_types=False)

        self.rebuild_components(redefine_indices=True, redefine_ids=(not keep_ids), redefine_names=True,
                                redefine_types=True)
        self.rebuild_chains(redefine_ids=(not keep_ids), redefine_types=True, redefine_names=False)

        self.rebuild_molecules(redefine_indices=False, redefine_ids=(not keep_ids), redefine_types=False,
                               redefine_names=True)
        self.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)
        self._coerce_id_columns_to_string()
        del tmp_item

    @signal(tags=['native'])
    def copy(self):
        """Return a deep copy of the topology tables."""

        tmp_item = Topology()

        tmp_item.atoms = self.atoms.copy()
        tmp_item.groups = self.groups.copy()
        tmp_item.molecules = self.molecules.copy()
        tmp_item.entities = self.entities.copy()
        tmp_item.chains = self.chains.copy()
        tmp_item._chemical_states = [state.copy() for state in self._chemical_states]
        tmp_item._reference_chemical_state_index = self._reference_chemical_state_index

        tmp_item._atoms_dirty = self._atoms_dirty
        tmp_item._groups_dirty = self._groups_dirty
        tmp_item._components_dirty = self._components_dirty
        tmp_item._molecules_dirty = self._molecules_dirty
        tmp_item._entities_dirty = self._entities_dirty
        tmp_item._chains_dirty = self._chains_dirty

        return tmp_item

    @signal(tags=['native'])
    def add_bonds(self, bonded_atom_pairs, skip_digestion=False):
        """Append new bonds given atom index pairs."""

        self._append_chemical_state_bonds(bonded_atom_pairs)

        self.rebuild_components(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)

    def remove_bonds(self, bond_indices='all', skip_digestion=False):
        """Drop bonds by index."""

        self._remove_chemical_state_bonds(bond_indices=bond_indices)

        self.rebuild_components(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)


    def add_missing_bonds(self, selection='all', syntax='MolSysMT', skip_digestion=False):
        """Infer and add missing bonds using geometric templates."""

        from molsysmt.build import get_missing_bonds as _get_missing_bonds

        bonds = _get_missing_bonds(self, selection=selection, syntax=syntax,
                                   engine='MolSysMT', with_templates=True, with_distances=False,
                                   skip_digestion=True)

        self.add_bonds(bonds, skip_digestion=True)

        self.rebuild_components(redefine_indices=True, redefine_ids=False, redefine_names=False, redefine_types=False)

    def rebuild_atoms(self, redefine_ids=True, redefine_types=True):
        """Regenerate atom ids/types from names and current counts."""

        if redefine_ids:

            self.atoms['atom_id']=np.arange(self.atoms.shape[0], dtype=int).astype(str)

        if redefine_types:

            from molsysmt.element.atom import get_atom_type_from_atom_name

            aux_dict = {}

            atom_types = []

            for atom_name in self.atoms['atom_name'].values:
                if atom_name not in aux_dict:
                    atom_type=get_atom_type_from_atom_name(atom_name)
                    aux_dict[atom_name]=atom_type
                    atom_types.append(atom_type)
                else:
                    atom_types.append(aux_dict[atom_name])

            self.atoms.atom_type = np.array(atom_types, dtype=object)

            del aux_dict, atom_types
        self._coerce_id_columns_to_string()

    def rebuild_groups(self, redefine_ids=True, redefine_types=True):
        """Rebuilding native group ids and locally inferred group types.

        Notes
        -----
        This is a native-only operation over the current `molsysmt.Topology`.
        It preserves existing group names, regenerates ids when requested, and
        infers group types only from local topology evidence.
        """

        if redefine_ids:

            self.groups['group_id']=np.arange(self.groups.shape[0], dtype=int).astype(str)

        if redefine_types:
            from ._topology_infer import infer_group_types_from_topology

            self.groups.group_type = infer_group_types_from_topology(self)
        self._coerce_id_columns_to_string()

    @signal(tags=['native'])
    def rebuild_components(self, redefine_indices=True, redefine_ids=True, redefine_types=True, redefine_names=True,
                           force=False):
        """Rebuilding native component membership and metadata from local evidence.

        Notes
        -----
        Component indices are inferred from connectivity. Component ids are
        synthesized as stable local string ids when requested. Component types
        and names are inferred from the current native group/component content.
        This method is a native API and is not form-agnostic.
        """
        from ._topology_infer import (
            _needs_columns,
            fallback_ids,
            infer_component_indices_from_topology,
            infer_component_names_from_topology,
            infer_component_types_from_topology,
        )

        if redefine_types and _needs_columns(self.groups, ["group_type"]):
            self.rebuild_groups(redefine_ids=False, redefine_types=True)

        need_component_indices = (redefine_names or redefine_types) and self._component_indices_are_missing()

        if redefine_indices or force or need_component_indices:
            component_index_of_atoms = infer_component_indices_from_topology(self)
            self._set_component_indices(component_index_of_atoms)

            if len(component_index_of_atoms) > 0:
                n_components = int(np.max(component_index_of_atoms)) + 1
            else:
                n_components = 0
            self.components = Components_DataFrame(n_components=n_components)

            del component_index_of_atoms

        if redefine_ids:
            self.components['component_id'] = fallback_ids(self.n_components)

        if redefine_types:
            self.components["component_type"] = infer_component_types_from_topology(self)

        if redefine_names:
            self.components["component_name"] = infer_component_names_from_topology(self)

        state = self._resolve_chemical_state()
        state.component_evidence = 'inferred'
        bonds = state.bonds
        participation_complete = (
            'joins_components' in bonds.columns
            and not bonds['joins_components'].isna().any()
        )
        if state.connectivity_completeness == 'complete' and participation_complete:
            state.component_completeness = 'complete'
        else:
            state.component_completeness = 'partial'
        
        self._components_dirty = False
        if redefine_indices or force:
            self._molecules_dirty = True

        self._coerce_id_columns_to_string()

    @signal(tags=['native'])
    def rebuild_molecules(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True,
                          molecules_as_components=True, force=False):
        """Rebuilding native molecule membership and metadata from local evidence.

        Notes
        -----
        When no better molecule definition is available, molecules fall back to
        components. Under that fallback, molecule name and type inherit from the
        corresponding component. This method is a native API and is not
        form-agnostic.
        """
        from ._topology_infer import (
            _needs_columns,
            fallback_ids,
            infer_molecule_indices_from_topology,
            infer_molecule_names_from_topology,
            infer_molecule_types_from_topology,
        )

        need_component_types = (redefine_names or redefine_types) and _needs_columns(self.components, ["component_type"])
        need_component_names = redefine_names and _needs_columns(self.components, ["component_name"])
        need_component_indices = (
            redefine_names or redefine_types or redefine_indices
        ) and self._component_indices_are_missing()
        if need_component_indices or need_component_types or need_component_names:
            self.rebuild_components(
                redefine_indices=need_component_indices,
                redefine_ids=False,
                redefine_types=(redefine_types or need_component_types or need_component_names),
                redefine_names=(redefine_names or need_component_names),
                force=need_component_indices,
            )

        need_molecule_indices = (redefine_names or redefine_types) and _needs_columns(self.groups, ["molecule_index"])

        if redefine_indices or force or need_molecule_indices:
            molecule_index_of_groups = infer_molecule_indices_from_topology(self)
            self.groups["molecule_index"] = molecule_index_of_groups.astype(int)
            if len(molecule_index_of_groups) > 0:
                n_molecules = int(np.max(molecule_index_of_groups)) + 1
            else:
                n_molecules = 0
            self.reset_molecules(n_molecules = n_molecules)

            del molecule_index_of_groups

        if redefine_ids:
            self.molecules["molecule_id"] = fallback_ids(self.n_molecules)

        # Types must be computed before names: infer_molecule_names_from_topology
        # reads molecule_type from the molecules DataFrame.
        if redefine_types:
            self.molecules["molecule_type"] = infer_molecule_types_from_topology(self)

        if redefine_names:
            self.molecules["molecule_name"] = infer_molecule_names_from_topology(self)

        self._molecules_dirty = False
        if redefine_indices or force:
            self._entities_dirty = True

        self._coerce_id_columns_to_string()

    @signal(tags=['native'])
    def rebuild_chains(self, redefine_indices=True, redefine_ids=True, redefine_types=True, redefine_names=True):
        """Rebuilding native chain membership and metadata from local evidence.

        Notes
        -----
        Chain indices are rebuilt from the current native atom/group assignment.
        Chain ids and names are regenerated as stable local values when
        requested. Chain types are inferred from locally available molecule
        types. This method is a native API and is not form-agnostic.
        """
        from ._topology_infer import (
            _needs_columns,
            infer_chain_ids_from_topology,
            infer_chain_indices_from_topology,
            infer_chain_names_from_topology,
            infer_chain_types_from_topology,
        )

        need_molecule_types = redefine_types and _needs_columns(self.molecules, ["molecule_type"])
        if need_molecule_types:
            self.rebuild_molecules(redefine_indices=False, redefine_ids=False, redefine_names=False, redefine_types=True)

        need_chain_indices = (redefine_names or redefine_types) and _needs_columns(self.atoms, ["chain_index"])

        if redefine_indices or need_chain_indices:
            chain_index_of_atoms = infer_chain_indices_from_topology(self)
            self.atoms["chain_index"] = np.array(chain_index_of_atoms, dtype=int)

            if len(chain_index_of_atoms) > 0:
                n_chains = int(np.max(chain_index_of_atoms)) + 1
            else:
                n_chains = 0
            self.reset_chains(n_chains = n_chains)

            del chain_index_of_atoms

        if redefine_ids:
            self.chains["chain_id"] = infer_chain_ids_from_topology(self)

        if redefine_types:
            self.chains["chain_type"] = infer_chain_types_from_topology(self)

        if redefine_names:
            self.chains["chain_name"] = infer_chain_names_from_topology(self)

        self._chains_dirty = False

        self._coerce_id_columns_to_string()


    @signal(tags=['native'])
    def rebuild_entities(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True,
                         force=False):
        """Rebuilding native entity membership and metadata from local evidence.

        Notes
        -----
        Entity membership is inferred from molecule-level information already
        present or rebuilt in the native topology. Water molecules are grouped
        under the same entity key. This method is a native API and is not
        form-agnostic.
        """
        from ._topology_infer import (
            _needs_columns,
            fallback_ids,
            infer_entity_indices_from_topology,
            infer_entity_names_from_topology,
            infer_entity_types_from_topology,
        )

        need_molecule_names = redefine_names and _needs_columns(self.molecules, ["molecule_name"])
        need_molecule_types = redefine_types and _needs_columns(self.molecules, ["molecule_type"])
        need_entity_indices = (redefine_names or redefine_types) and _needs_columns(self.molecules, ["entity_index"])
        if need_molecule_names or need_molecule_types or need_entity_indices:
            self.rebuild_molecules(
                redefine_indices=False,
                redefine_ids=False,
                redefine_names=(redefine_names or need_molecule_names),
                redefine_types=(redefine_types or need_molecule_types),
            )

        if redefine_indices or force or need_entity_indices:
            entity_index_of_molecules = infer_entity_indices_from_topology(self)
            self.molecules["entity_index"] = entity_index_of_molecules.astype(int)
            if len(entity_index_of_molecules) > 0:
                n_entities = int(np.max(entity_index_of_molecules)) + 1
            else:
                n_entities = 0
            self.reset_entities(n_entities = n_entities)

            del entity_index_of_molecules

        if redefine_ids:
            self.entities["entity_id"] = fallback_ids(self.n_entities)

        if redefine_names:
            self.entities["entity_name"] = infer_entity_names_from_topology(self)

        if redefine_types:
            self.entities["entity_type"] = infer_entity_types_from_topology(self)
        
        self._entities_dirty = False

        self._coerce_id_columns_to_string()

    def _join_molecules(self, indices=None):
        """Merge multiple molecules into a single entry."""
        raise NotImplementedError

    def _fix_null_values(self):
        """Normalize null values across all tables."""

        self.atoms._fix_null_values()
        self.groups._fix_null_values()
        self.components._fix_null_values()
        self.molecules._fix_null_values()
        self.entities._fix_null_values()
        self.chains._fix_null_values()
        self._get_chemical_state_bonds()._fix_null_values()
        self._coerce_id_columns_to_string()

    def _sort_bonds(self):
        """Sort bond table in place."""

        self._get_chemical_state_bonds()._sort_bonds()

    @arg_digest()
    def compare(self, item, rule='equal', output_type='boolean', skip_digestion=False, **kwargs):
        """Compare topology content with another topology."""

        if rule == 'equal':

            output = {}

            if 'n_atoms' in kwargs:

                tmp_output = (self.atoms.shape[0]==item.atoms.shape[0])
                output['n_atoms'] = (kwargs['n_atoms'] == tmp_output)

            if 'atom_index' in kwargs:

                tmp_output = (self.atoms.shape[0]==item.atoms.shape[0])
                output['atom_index'] = (kwargs['atom_index'] == tmp_output)

            if 'atom_id' in kwargs:

                tmp_output = (self.atoms['atom_id'].values==item.atoms['atom_id'].values).all()
                output['atom_id'] = (kwargs['atom_id'] == tmp_output)

            if 'atom_name' in kwargs:

                tmp_output = (self.atoms['atom_name'].values==item.atoms['atom_name'].values).all()
                output['atom_name'] = (kwargs['atom_name'] == tmp_output)

            if 'atom_type' in kwargs:

                tmp_output = (self.atoms['atom_type'].values==item.atoms['atom_type'].values).all()
                output['atom_type'] = (kwargs['atom_type'] == tmp_output)

            if 'n_groups' in kwargs:

                tmp_output = (self.groups.shape[0]==item.groups.shape[0])
                output['n_groups'] = (kwargs['n_groups'] == tmp_output)

            if 'group_index' in kwargs:

                tmp_output = (self.atoms['group_index'].values==item.atoms['group_index'].values).all()
                output['group_index'] = (kwargs['group_index'] == tmp_output)

            if 'group_id' in kwargs:

                tmp_output = (self.groups['group_id'].values==item.groups['group_id'].values).all()
                output['group_id'] = (kwargs['group_id'] == tmp_output)

            if 'group_name' in kwargs:

                tmp_output = (self.groups['group_name'].values==item.groups['group_name'].values).all()
                output['group_name'] = (kwargs['group_name'] == tmp_output)

            if 'group_type' in kwargs:

                tmp_output = (self.groups['group_type'].values==item.groups['group_type'].values).all()
                output['group_type'] = (kwargs['group_type'] == tmp_output)

            if 'component_index' in kwargs:

                tmp_output = (
                    self._get_component_indices().values == item._get_component_indices().values
                ).all()
                output['component_index'] = (kwargs['component_index'] == tmp_output)

            if 'component_id' in kwargs:

                tmp_output = (self.components['component_id'].values==item.components['component_id'].values).all()
                output['component_id'] = (kwargs['component_id'] == tmp_output)

            if 'component_name' in kwargs:

                tmp_output = (self.components['component_name'].values==item.components['component_name'].values).all()
                output['component_name'] = (kwargs['component_name'] == tmp_output)

            if 'component_type' in kwargs:

                tmp_output = (self.components['component_type'].values==item.components['component_type'].values).all()
                output['component_type'] = (kwargs['component_type'] == tmp_output)

            if 'molecule_index' in kwargs:

                tmp_output = (self.groups['molecule_index'].values==item.groups['molecule_index'].values).all()
                output['molecule_index'] = (kwargs['molecule_index'] == tmp_output)

            if 'molecule_id' in kwargs:

                tmp_output = (self.molecules['molecule_id'].values==item.molecules['molecule_id'].values).all()
                output['molecule_id'] = (kwargs['molecule_id'] == tmp_output)

            if 'molecule_name' in kwargs:

                tmp_output = (self.molecules['molecule_name'].values==item.molecules['molecule_name'].values).all()
                output['molecule_name'] = (kwargs['molecule_name'] == tmp_output)

            if 'molecule_type' in kwargs:

                tmp_output = (self.molecules['molecule_type'].values==item.molecules['molecule_type'].values).all()
                output['molecule_type'] = (kwargs['molecule_type'] == tmp_output)

            if 'entity_index' in kwargs:

                tmp_output = (self.molecules['entity_index'].values==item.molecules['entity_index'].values).all()
                output['entity_index'] = (kwargs['entity_index'] == tmp_output)

            if 'entity_id' in kwargs:

                tmp_output = (self.entities['entity_id'].values==item.entities['entity_id'].values).all()
                output['entity_id'] = (kwargs['entity_id'] == tmp_output)

            if 'entity_name' in kwargs:

                tmp_output = (self.entities['entity_name'].values==item.entities['entity_name'].values).all()
                output['entity_name'] = (kwargs['entity_name'] == tmp_output)

            if 'entity_type' in kwargs:

                tmp_output = (self.entities['entity_type'].values==item.entities['entity_type'].values).all()
                output['entity_type'] = (kwargs['entity_type'] == tmp_output)

            if 'chain_index' in kwargs:

                tmp_output = (self.atoms['chain_index'].values==item.atoms['chain_index'].values).all()
                output['chain_index'] = (kwargs['chain_index'] == tmp_output)

            if 'chain_id' in kwargs:

                tmp_output = (self.chains['chain_id'].values==item.chains['chain_id'].values).all()
                output['chain_id'] = (kwargs['chain_id'] == tmp_output)

            if 'chain_name' in kwargs:

                tmp_output = (self.chains['chain_name'].values==item.chains['chain_name'].values).all()
                output['chain_name'] = (kwargs['chain_name'] == tmp_output)

            if 'chain_type' in kwargs:

                tmp_output = (self.chains['chain_type'].values==item.chains['chain_type'].values).all()
                output['chain_type'] = (kwargs['chain_type'] == tmp_output)

            if 'n_bonds' in kwargs:

                tmp_output = (
                    self._get_chemical_state_bonds().shape[0]
                    == item._get_chemical_state_bonds().shape[0]
                )
                output['n_bonds'] = (kwargs['n_bonds'] == tmp_output)

            if 'bonded_atom_pairs' in kwargs:

                bonds = self._get_chemical_state_bonds()
                item_bonds = item._get_chemical_state_bonds()
                tmp_output1 = (bonds['atom1_index'] == item_bonds['atom1_index']).all()
                tmp_output2 = (bonds['atom2_index'] == item_bonds['atom2_index']).all()
                tmp_output = tmp_output1*tmp_output2
                output['bonded_atom_pairs'] = (kwargs['bonded_atom_pairs'] == tmp_output)

        if output_type=='boolean':
            output = all(list(output.values()))

        return output

    def get_atom_indices(self, **kwargs):
        """Select atom indices matching the provided hierarchical filters."""

        for aux in kwargs:
            if isinstance(kwargs[aux], (str, int)):
                kwargs[aux] = [kwargs[aux]]
            if aux.endswith('_id') and kwargs[aux] is not None:
                kwargs[aux] = [str(ii) for ii in kwargs[aux]]

        atom_columns = []
        group_columns = []
        component_columns = []
        molecule_columns = []
        entity_columns = []
        chain_columns = []

        for aux in self.atoms.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    atom_columns.append(aux)

        for aux in self.groups.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    group_columns.append(aux)

        for aux in self.components.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    component_columns.append(aux)

        for aux in self.molecules.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    molecule_columns.append(aux)

        for aux in self.entities.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    entity_columns.append(aux)

        for aux in self.chains.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    chain_columns.append(aux)

        if len(entity_columns):
            if 'entity_index' not in molecule_columns:
                molecule_columns.append('entity_index')

        if len(molecule_columns):
            if 'molecule_index' not in group_columns:
                group_columns.append('molecule_index')

        if len(group_columns):
            if 'group_index' not in atom_columns:
                atom_columns.append('group_index')

        if len(component_columns):
            if 'component_index' not in atom_columns:
                atom_columns.append('component_index')

        if len(chain_columns):
            if 'chain_index' not in atom_columns:
                atom_columns.append('chain_index')

        from molsysmt._private.topology_expansion import expand_atom_dataframe

        aux_df = expand_atom_dataframe(
            self,
            atom_columns=atom_columns,
            group_columns=group_columns,
            component_columns=component_columns,
            molecule_columns=molecule_columns,
            entity_columns=entity_columns,
            chain_columns=chain_columns,
        )

        mask = pd.Series(True, index=aux_df.index)

        for col, valores in kwargs.items():
            mask &= aux_df[col].isin(valores)

        return aux_df.index[mask].tolist()
