from contextlib import contextmanager, nullcontext
from contextvars import ContextVar

import numpy as np
import pandas as pd
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.variables import is_all

from . import _chemical_state as _chemical_storage
from .chemical_states import ChemicalStates
from .queries import NativeQueries

# Transitional private bindings keep existing callers and legacy pickle paths
# working while #255 migrates them. ChemicalStates uses the canonical owner.
Bonds_DataFrame = _chemical_storage.Bonds_DataFrame
Components_DataFrame = _chemical_storage.Components_DataFrame
_BOND_ALLOWED_COLUMNS = _chemical_storage._BOND_ALLOWED_COLUMNS
_BOND_ATOM_REFERENCE_COLUMNS = _chemical_storage._BOND_ATOM_REFERENCE_COLUMNS
_BOND_OPTIONAL_DTYPES = _chemical_storage._BOND_OPTIONAL_DTYPES
_BOND_REQUIRED_COLUMNS = _chemical_storage._BOND_REQUIRED_COLUMNS
_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES = (
    _chemical_storage._CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES
)
_CHEMICAL_STATE_ATOM_STEREOCHEMISTRY_VALUES = (
    _chemical_storage._CHEMICAL_STATE_ATOM_STEREOCHEMISTRY_VALUES
)
_CHEMICAL_STATE_COMPLETENESS_VALUES = (
    _chemical_storage._CHEMICAL_STATE_COMPLETENESS_VALUES
)
_CHEMICAL_STATE_EVIDENCE_VALUES = _chemical_storage._CHEMICAL_STATE_EVIDENCE_VALUES
_ChemicalStateStorage = _chemical_storage._ChemicalStateStorage

_ACTIVE_CHEMICAL_STATE_INDICES = ContextVar(
    "molsysmt_active_chemical_state_indices", default={}
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

_ATOMS_COLUMNS = frozenset(
    ["atom_id", "atom_name", "atom_type", "isotope", "group_index", "chain_index"]
)
_GROUPS_COLUMNS = frozenset(["group_id", "group_name", "group_type", "molecule_index"])


class Atoms_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing atom-level topology fields.

    Schema (fixed): atom_id, atom_name, atom_type, isotope, group_index, chain_index.
    """

    def __init__(self, n_atoms=0):
        columns = [
            "atom_id",
            "atom_name",
            "atom_type",
            "isotope",
            "group_index",
            "chain_index",
        ]
        super().__init__(index=range(n_atoms), columns=columns)
        self["atom_id"] = self["atom_id"].astype("string")
        self["atom_name"] = self["atom_name"].astype(str)
        self["atom_type"] = self["atom_type"].astype(str)
        self["isotope"] = self["isotope"].astype("UInt16")
        self["group_index"] = self["group_index"].astype("Int64")
        self["chain_index"] = self["chain_index"].astype("Int64")

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
        self["atom_id"] = self["atom_id"].astype("string")
        self["isotope"] = self["isotope"].astype("UInt16")


class Groups_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing group-level topology fields.

    Schema (fixed): group_id, group_name, group_type, molecule_index.

    component_index and chain_index are NOT group-level attributes. Component
    membership is atom-aligned chemical-state data. Chain membership lives on
    stable atoms, with an optional separate ordered chain/group declaration.
    Writing either column here raises AttributeError.
    """

    def __init__(self, n_groups=0):
        columns = ["group_id", "group_name", "group_type", "molecule_index"]
        super().__init__(index=range(n_groups), columns=columns)
        self["group_id"] = self["group_id"].astype("string")
        self["group_name"] = self["group_name"].astype(str)
        self["group_type"] = self["group_type"].astype(str)
        self["molecule_index"] = self["molecule_index"].astype("Int64")

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
        self["group_id"] = self["group_id"].astype("string")


class Molecules_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing molecule-level fields."""

    def __init__(self, n_molecules=0):
        """Initialize a molecules table with default types."""

        columns = ["molecule_id", "molecule_name", "molecule_type", "entity_index"]

        super().__init__(index=range(n_molecules), columns=columns)

        self["molecule_id"] = self["molecule_id"].astype("string")
        self["molecule_name"] = self["molecule_name"].astype(str)
        self["molecule_type"] = self["molecule_type"].astype(str)
        self["entity_index"] = self["entity_index"].astype("Int64")

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column] = self[column].fillna(pd.NA)
        self["molecule_id"] = self["molecule_id"].astype("string")


class Entities_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing entity-level fields."""

    def __init__(self, n_entities=0):
        """Initialize an entities table with default types."""

        columns = ["entity_id", "entity_name", "entity_type"]

        super().__init__(index=range(n_entities), columns=columns)

        self["entity_id"] = self["entity_id"].astype("string")
        self["entity_name"] = self["entity_name"].astype(str)
        self["entity_type"] = self["entity_type"].astype(str)

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column] = self[column].fillna(pd.NA)
        self["entity_id"] = self["entity_id"].astype("string")


class Chains_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing chain-level fields."""

    def __init__(self, n_chains=0):
        """Initialize a chains table with default types."""

        columns = ["chain_id", "chain_name", "chain_type"]

        super().__init__(index=range(n_chains), columns=columns)

        self["chain_id"] = self["chain_id"].astype("string")
        self["chain_name"] = self["chain_name"].astype(str)
        self["chain_type"] = self["chain_type"].astype(str)

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column] = self[column].fillna(pd.NA)
        self["chain_id"] = self["chain_id"].astype("string")


# Keeping the old private class name allows pickles produced during the staged
# migration to resolve their original class reference.
_ReferenceChemicalStateStorage = _ChemicalStateStorage


class Topology(NativeQueries):
    """Holding a stable atom inventory with chemical-state compatibility access.

    Subclasses inheriting the constructor retain its native count validation,
    including when the subclass is defined in another module. Ordinary user
    construction does not require skip_digestion.
    """

    def __repr__(self):
        """Summarizing stored metadata without reading or rendering payloads."""
        from ._repr import summary, topology_fields

        return summary(self, **topology_fields(self))

    def __setattr__(self, name, value):
        if name == "chemical_states":
            raise AttributeError(
                "Topology has no chemical_states attribute; assign chemical states "
                "through MolSys.chemical_states."
            )
        super().__setattr__(name, value)

    def __getstate__(self):
        """Exclude a MolSys ownership link from topology serialization."""

        state = self.__dict__.copy()
        state.pop("_molsys_owner_ref", None)
        return state

    def __copy__(self):
        """Copying independent topology state without retaining its owner link."""
        return self.__deepcopy__({})

    def __deepcopy__(self, memo):
        """Copying current tables and chemistry without legacy restoration."""
        from ._copy import _clone

        return _clone(self, memo, exclude=("_molsys_owner_ref",))

    @property
    def _chemical_states(self):
        return self._chemical_states_domain._states

    @_chemical_states.setter
    def _chemical_states(self, value):
        self._chemical_states_domain._replace_states(
            value, self._chemical_states_domain._reference_index
        )

    @property
    def _reference_chemical_state_index(self):
        return self._chemical_states_domain._reference_index

    @_reference_chemical_state_index.setter
    def _reference_chemical_state_index(self, value):
        self._chemical_states_domain._set_reference_index(value)

    @arg_digest(native_constructor="molsysmt.native.topology.__init__")
    def __init__(
        self,
        n_atoms=0,
        n_groups=0,
        n_components=0,
        n_molecules=0,
        n_entities=0,
        n_chains=0,
        n_bonds=0,
        skip_digestion=False,
    ):
        """Initialize empty topology tables with the requested sizes."""

        self._chemical_states_domain = ChemicalStates(
            n_atoms=n_atoms, skip_digestion=True
        )
        self._chemical_states_domain._append_state(
            _ChemicalStateStorage(n_atoms=n_atoms), set_as_reference=True
        )
        self.reset_atoms(n_atoms=n_atoms)
        self.reset_groups(n_groups=n_groups)
        self.reset_components(n_components=n_components)
        self.reset_molecules(n_molecules=n_molecules)
        self.reset_entities(n_entities=n_entities)
        self.reset_chains(n_chains=n_chains)
        self.reset_bonds(n_bonds=n_bonds)
        self._chain_group_membership = None
        self._atom_molecule_membership = None
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

        if not hasattr(self, "_chemical_states") or len(self._chemical_states) == 0:
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
                reason="Topology has no chemical state; state-dependent data are unavailable.",
                caller="molsysmt.native.Topology",
            )
        if n_states == 1:
            return 0
        state_index = self._reference_chemical_state_index
        if state_index is None:
            raise StructuralInconsistencyError(
                reason=(
                    f"Topology has {n_states} chemical states and no reference state; "
                    "state-dependent access is ambiguous."
                ),
                caller="molsysmt.native.Topology",
            )
        if (
            not isinstance(state_index, (int, np.integer))
            or not 0 <= int(state_index) < n_states
        ):
            raise StructuralInconsistencyError(
                reason=f"Reference chemical-state index {state_index!r} is invalid for {n_states} states.",
                caller="molsysmt.native.Topology",
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
                reason="Chemical-state index must be an integer or None.",
                caller="molsysmt.native.Topology",
            )
        state_index = int(state_index)
        if not 0 <= state_index < len(self._chemical_states):
            raise StructuralInconsistencyError(
                reason=f"Chemical-state index {state_index} is invalid for {len(self._chemical_states)} states.",
                caller="molsysmt.native.Topology",
            )
        return self._chemical_states[state_index]

    def _chemical_state_inventory_equals(self, item):
        """Return whether stable atoms and ordered chemical states match exactly."""

        if not isinstance(item, Topology):
            return False
        first = getattr(self, "_atom_molecule_membership", None)
        second = getattr(item, "_atom_molecule_membership", None)
        if (
            (first is None) != (second is None)
            or first is not None
            and not np.array_equal(first, second)
        ):
            return False
        for table_name in ("atoms", "groups", "molecules", "entities", "chains"):
            if not getattr(self, table_name).equals(getattr(item, table_name)):
                return False
        return self._chemical_states_domain._inventory_equals(
            item._chemical_states_domain
        )

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

    def _has_chemical_state_atom_attribute(
        self, name, state_index=None, include_none=False
    ):
        """Return private instance availability for an atom-state attribute."""

        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        return state.has_atom_attribute(name, include_none=include_none)

    def _get_chemical_state_atom_attribute(
        self, name, atom_indices=None, state_index=None
    ):
        """Return one private atom-state attribute from a resolved state."""

        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        return state.get_atom_attribute(name, atom_indices=atom_indices)

    def _set_chemical_state_atom_attribute(
        self, name, values, atom_indices=None, state_index=None
    ):
        """Set one private atom-state attribute on a resolved state."""

        if atom_indices is not None and np.asarray(atom_indices).size == 0:
            return
        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        candidate = state._prepare_atom_attribute(name, values, atom_indices)
        with self._invalidating_chemical_interactions():
            state.atom_attributes = candidate

    def _invalidating_chemical_interactions(self, changed=True):
        """Stage conservative owner invalidation for a prepared chemical edit."""
        owner_ref = getattr(self, "_molsys_owner_ref", None)
        owner = None if owner_ref is None else owner_ref()
        if not changed or owner is None:
            return nullcontext()
        return owner._invalidating_interaction_frames("all")

    def _remove_chemical_state_atom_attribute(self, name, state_index=None):
        """Remove one private optional atom-state attribute."""

        state = self._resolve_chemical_state(state_index=state_index)
        if name not in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES:
            state.remove_atom_attribute(name)
            return
        if name in state.atom_attributes.columns:
            candidate = state.atom_attributes.drop(columns=name)
            with self._invalidating_chemical_interactions():
                state.atom_attributes = candidate

    _coerce_bond_table = staticmethod(_chemical_storage._coerce_bond_table)

    _concatenate_bond_tables = staticmethod(_chemical_storage._concatenate_bond_tables)

    _remap_bond_atom_indices = staticmethod(_chemical_storage._remap_bond_atom_indices)

    def _get_chemical_state_bonds(self, state_index=None):
        """Return the single authoritative bond table for a resolved state."""

        return self._resolve_chemical_state(state_index=state_index).bonds

    def _set_chemical_state_bond_attribute(
        self, name, values, bond_indices="all", state_index=None
    ):
        """Set one normalized bond field on all or selected bonds atomically."""

        if name not in _BOND_OPTIONAL_DTYPES:
            raise StructuralInconsistencyError(
                reason=f"Unsupported canonical bond attribute {name!r}.",
                caller="molsysmt.native.Topology",
            )
        bonds = self._get_chemical_state_bonds(state_index=state_index).copy()
        if is_all(bond_indices):
            indices = np.arange(len(bonds), dtype=np.int64)
        else:
            indices = np.asarray(bond_indices, dtype=np.int64)
            if (
                indices.ndim != 1
                or np.any(indices < 0)
                or np.any(indices >= len(bonds))
            ):
                raise StructuralInconsistencyError(
                    reason="Bond indices for chemical-state assignment are out of range.",
                    caller="molsysmt.native.Topology",
                )

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
                    caller="molsysmt.native.Topology",
                )

        if not len(indices):
            return

        if name not in bonds.columns:
            bonds[name] = pd.array(
                [pd.NA] * len(bonds), dtype=_BOND_OPTIONAL_DTYPES[name]
            )
        bonds.loc[indices, name] = pd.array(
            normalized, dtype=_BOND_OPTIONAL_DTYPES[name]
        )
        self._set_chemical_state_bonds(bonds, state_index=state_index)

    def _set_chemical_state_bond_stereo_atom_indices(
        self, values, bond_indices="all", state_index=None
    ):
        """Set the two stereo-reference atom indices as one public attribute."""

        bonds = self._get_chemical_state_bonds(state_index=state_index).copy()
        if is_all(bond_indices):
            indices = np.arange(len(bonds), dtype=np.int64)
        else:
            indices = np.asarray(bond_indices, dtype=np.int64)
            if (
                indices.ndim != 1
                or np.any(indices < 0)
                or np.any(indices >= len(bonds))
            ):
                raise StructuralInconsistencyError(
                    reason="Bond indices for stereo-reference assignment are out of range.",
                    caller="molsysmt.native.Topology",
                )

        if not len(indices):
            return

        if values is None or values is pd.NA:
            normalized = [[pd.NA, pd.NA] for _ in indices]
        else:
            normalized = np.asarray(values, dtype=object)
            if normalized.ndim == 1 and len(indices) == 1 and normalized.shape == (2,):
                normalized = normalized.reshape(1, 2)
            if normalized.shape != (len(indices), 2):
                raise StructuralInconsistencyError(
                    reason=(
                        f"bond_stereo_atom_indices must have shape ({len(indices)}, 2)."
                    ),
                    caller="molsysmt.native.Topology",
                )

        for column, column_values in zip(
            ("stereo_atom1_index", "stereo_atom2_index"), np.asarray(normalized).T
        ):
            if column not in bonds.columns:
                bonds[column] = pd.array([pd.NA] * len(bonds), dtype="Int64")
            bonds.loc[indices, column] = pd.array(column_values, dtype="Int64")
        self._set_chemical_state_bonds(bonds, state_index=state_index)

    def _set_chemical_state_bonds(self, value, state_index=None):
        """Replace the authoritative bond table without reinterpreting metadata."""

        candidate = self._coerce_bond_table(value, n_atoms=self.n_atoms)
        self._publish_chemical_state_bonds(candidate, state_index)

    def _publish_chemical_state_bonds(
        self, candidate, state_index=None, *, declared_edges=True
    ):
        """Publish prepared bonds after staging owner invalidation, ignoring labels."""
        state = (
            None
            if state_index is None and not self._chemical_states
            else self._resolve_chemical_state(state_index=state_index)
        )
        columns = tuple(name for name in candidate.columns if name != "bond_id")
        changed = (
            state is None
            or columns
            != tuple(name for name in state.bonds.columns if name != "bond_id")
            or any(not state.bonds[name].equals(candidate[name]) for name in columns)
        )
        with self._invalidating_chemical_interactions(changed):
            if state is None:
                state = self._ensure_state_for_mutation()
            state.bonds = candidate
            if (
                declared_edges
                and len(candidate)
                and state.connectivity_completeness == "unavailable"
            ):
                state.connectivity_completeness = "partial"

    def _reset_chemical_state_bonds(self, n_bonds=0, state_index=None):
        """Reset one state's bond table, allowing explicit construction rows."""

        self._publish_chemical_state_bonds(
            Bonds_DataFrame(n_bonds=n_bonds), state_index, declared_edges=False
        )

    def _append_chemical_state_bonds(
        self,
        bonded_atom_pairs,
        orders=None,
        types=None,
        state_index=None,
        sort=True,
        **metadata,
    ):
        """Append normalized or explicitly translated legacy bond rows."""

        bonded_atom_pairs = np.asarray(bonded_atom_pairs)
        if bonded_atom_pairs.size == 0:
            bonded_atom_pairs = np.empty((0, 2), dtype=int)
        if bonded_atom_pairs.ndim != 2 or bonded_atom_pairs.shape[1] != 2:
            raise StructuralInconsistencyError(
                reason="Bonded atom pairs must have shape (n_bonds, 2).",
                caller="molsysmt.native.Topology",
            )
        try:
            bonded_atom_pairs = bonded_atom_pairs.astype(int, copy=False)
        except (TypeError, ValueError, OverflowError) as error:
            raise StructuralInconsistencyError(
                reason=f"Bonded atom indices must be integers: {error}",
                caller="molsysmt.native.Topology",
            )

        if bonded_atom_pairs.size:
            if np.any(bonded_atom_pairs < 0) or np.any(
                bonded_atom_pairs >= self.n_atoms
            ):
                raise StructuralInconsistencyError(
                    reason=f"Bonded atom indices must be between 0 and {self.n_atoms - 1}.",
                    caller="molsysmt.native.Topology",
                )

        n_new_bonds = bonded_atom_pairs.shape[0]
        if not n_new_bonds:
            return

        def _metadata_values(values, field):
            if values is None:
                return [pd.NA] * n_new_bonds
            if np.isscalar(values) or values is pd.NA:
                return [values] * n_new_bonds
            values = list(values)
            if len(values) != n_new_bonds:
                raise StructuralInconsistencyError(
                    reason=f"Bond {field} received {len(values)} values; expected {n_new_bonds}.",
                    caller="molsysmt.native.Topology",
                )
            return values

        unexpected_metadata = set(metadata) - set(_BOND_OPTIONAL_DTYPES)
        if unexpected_metadata:
            raise StructuralInconsistencyError(
                reason=f"Unsupported bond metadata fields: {sorted(unexpected_metadata)}.",
                caller="molsysmt.native.Topology",
            )

        new_bonds = pd.DataFrame(
            {
                "atom1_index": bonded_atom_pairs[:, 0],
                "atom2_index": bonded_atom_pairs[:, 1],
            }
        )
        if orders is not None:
            new_bonds["order"] = _metadata_values(orders, "order")
        if types is not None:
            new_bonds["type"] = _metadata_values(types, "type")
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
            combined.index = pd.RangeIndex(len(combined))
        self._set_chemical_state_bonds(combined, state_index=state_index)
        if n_new_bonds and state.connectivity_completeness == "unavailable":
            state.connectivity_completeness = "partial"

    def _remove_chemical_state_bonds(self, bond_indices="all", state_index=None):
        """Remove bond rows from a resolved state through the storage seam."""

        bonds = self._get_chemical_state_bonds(state_index=state_index)
        if is_all(bond_indices):
            self._reset_chemical_state_bonds(n_bonds=0, state_index=state_index)
            return
        if np.asarray(bond_indices).size == 0:
            return
        candidate = bonds.drop(bond_indices).reset_index(drop=True)
        candidate = self._coerce_bond_table(candidate, n_atoms=self.n_atoms)
        self._publish_chemical_state_bonds(candidate, state_index, declared_edges=False)

    def _append_chemical_state(self, state_id=None, set_as_reference=False):
        """Append an empty private chemical state and return its index."""

        state = _ChemicalStateStorage(n_atoms=self.n_atoms, state_id=state_id)
        return self._chemical_states_domain._append_state(state, set_as_reference)

    def _clear_chemical_states(self):
        """Remove all private chemical states without changing stable topology."""

        self._chemical_states_domain._replace_states([], None)

    def _set_reference_chemical_state_index(self, state_index):
        """Set the private reference-state index after validating it."""

        self._chemical_states_domain._set_reference_index(state_index)

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
        """Replacing reference-state bonds after validating canonical chemistry.

        Scientific changes invalidate every named analysis in the owning MolSys.
        Bond-label-only changes preserve analyses. Previously held tables and
        interaction snapshots remain independent of this replacement.
        """

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

        state.pop("_molsys_owner_ref", None)

        if "atoms_dataframe" in state:
            self._restore_legacy_flat_state(state)
            return

        legacy_component_indices = None
        legacy_atoms = state.get("atoms")
        if legacy_atoms is not None and "component_index" in legacy_atoms.columns:
            legacy_component_indices = legacy_atoms["component_index"].copy()
            legacy_atoms = legacy_atoms.drop(columns="component_index")
            state["atoms"] = legacy_atoms

        legacy_bonds = state.pop("bonds", None)
        legacy_molecule_membership = "_atom_molecule_membership" not in state
        legacy_components = state.pop("components", None)
        legacy_reference_state = state.pop("_reference_chemical_state", None)
        legacy_states = state.pop("_chemical_states", None)
        had_legacy_reference_index = "_reference_chemical_state_index" in state
        legacy_reference_index = state.pop("_reference_chemical_state_index", None)
        self.__dict__.update(state)
        if legacy_molecule_membership:
            self._atom_molecule_membership = None
        if "_chemical_states_domain" not in self.__dict__:
            self._chemical_states_domain = ChemicalStates(
                n_atoms=self.n_atoms, skip_digestion=True
            )
            if legacy_states is not None:
                self._chemical_states = legacy_states
                self._reference_chemical_state_index = (
                    legacy_reference_index
                    if had_legacy_reference_index
                    else (0 if len(legacy_states) == 1 else None)
                )
        if "isotope" not in self.atoms.columns:
            self.atoms.insert(
                3, "isotope", pd.array([pd.NA] * self.n_atoms, dtype="UInt16")
            )

        if not self._chemical_states and legacy_states is None:
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

        if (
            self._reference_chemical_state_index is None
            and len(self._chemical_states) == 1
        ):
            self._reference_chemical_state_index = (
                0 if len(self._chemical_states) == 1 else None
            )

        if legacy_component_indices is not None and len(self._chemical_states):
            reference_index = self._resolve_reference_chemical_state_index()
            reference_state = self._chemical_states[reference_index]
            if reference_state.component_indices.isna().all():
                reference_state.component_indices = pd.Series(
                    pd.array(legacy_component_indices, dtype="Int64"),
                    index=range(self.n_atoms),
                )

        if legacy_bonds is not None:
            self._set_chemical_state_bonds(legacy_bonds)
        if legacy_components is not None:
            self._ensure_state_for_mutation().components = legacy_components
        if legacy_molecule_membership:
            from ._legacy_molecule_membership import restore

            restore(self, self._chemical_states_domain)

    def _restore_legacy_flat_state(self, state):
        """Restore the pre-normalization flat atom and bond tables."""

        legacy_atoms = state["atoms_dataframe"].copy()
        legacy_bonds = state.get("bonds_dataframe")
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
            element: index_map(f"{element}_index")
            for element in ("group", "component", "molecule", "entity", "chain")
        }
        restored = type(self)(
            n_atoms=n_atoms,
            n_groups=len(maps["group"]),
            n_components=len(maps["component"]),
            n_molecules=len(maps["molecule"]),
            n_entities=len(maps["entity"]),
            n_chains=len(maps["chain"]),
            skip_digestion=True,
        )
        self.__dict__.update(restored.__dict__)

        def values(column, default=None):
            if column in legacy_atoms:
                return legacy_atoms[column].tolist()
            return [default] * n_atoms

        self.atoms["atom_id"] = values("atom_id")
        self.atoms["atom_name"] = values("atom_name")
        self.atoms["atom_type"] = values("atom_type")
        self.atoms["isotope"] = pd.array(values("isotope"), dtype="UInt16")
        for element in ("group", "component", "chain"):
            column = f"{element}_index"
            mapped = [
                maps[element].get(value, pd.NA) if pd.notna(value) else pd.NA
                for value in values(column)
            ]
            if element == "component":
                self._set_component_indices(mapped)
            else:
                self.atoms[column] = mapped

        def fill_table(element, table, columns):
            source_index = f"{element}_index"
            for old_index, new_index in maps[element].items():
                row = legacy_atoms.loc[legacy_atoms[source_index] == old_index].iloc[0]
                for target_column, source_column in columns.items():
                    if source_column in legacy_atoms:
                        value = row[source_column]
                        if target_column.endswith("_id") and pd.notna(value):
                            value = str(value)
                        table.loc[new_index, target_column] = value

        fill_table(
            "component",
            self.components,
            {
                "component_id": "component_id",
                "component_name": "component_name",
                "component_type": "component_type",
            },
        )
        fill_table(
            "entity",
            self.entities,
            {
                "entity_id": "entity_id",
                "entity_name": "entity_name",
                "entity_type": "entity_type",
            },
        )
        fill_table(
            "chain",
            self.chains,
            {
                "chain_id": "chain_id",
                "chain_name": "chain_name",
                "chain_type": "chain_type",
            },
        )
        fill_table(
            "molecule",
            self.molecules,
            {
                "molecule_id": "molecule_id",
                "molecule_name": "molecule_name",
                "molecule_type": "molecule_type",
            },
        )
        fill_table(
            "group",
            self.groups,
            {
                "group_id": "group_id",
                "group_name": "group_name",
                "group_type": "group_type",
            },
        )

        for old_index, new_index in maps["group"].items():
            row = legacy_atoms.loc[legacy_atoms["group_index"] == old_index].iloc[0]
            molecule_index = row.get("molecule_index", pd.NA)
            self.groups.loc[new_index, "molecule_index"] = maps["molecule"].get(
                molecule_index, pd.NA
            )
        for old_index, new_index in maps["molecule"].items():
            row = legacy_atoms.loc[legacy_atoms["molecule_index"] == old_index].iloc[0]
            entity_index = row.get("entity_index", pd.NA)
            self.molecules.loc[new_index, "entity_index"] = maps["entity"].get(
                entity_index, pd.NA
            )

        if legacy_bonds is not None:
            atom_labels = values("atom_index")
            if len(set(atom_labels)) != n_atoms:
                raise StructuralInconsistencyError(
                    reason="Legacy serialized atom indices are not unique.",
                    caller="molsysmt.native.Topology.__setstate__",
                )
            atom_map = {label: index for index, label in enumerate(atom_labels)}
            migrated_bonds = legacy_bonds.copy()
            for endpoint in ("atom1_index", "atom2_index"):
                migrated_bonds[endpoint] = [
                    atom_map[value] for value in migrated_bonds[endpoint]
                ]
            self._set_chemical_state_bonds(migrated_bonds)
            self._get_chemical_state_bonds()._sort_bonds()
            self._reference_chemical_state.connectivity_completeness = "partial"

        component_values = values("component_index")
        if component_values and all(pd.notna(value) for value in component_values):
            self._reference_chemical_state.component_completeness = "complete"
        self._reference_chemical_state.component_evidence = "unknown"
        if "molecule_index" in legacy_atoms:
            from ._atom_molecules import compact

            direct = np.asarray(
                [
                    maps["molecule"].get(value, -1) if pd.notna(value) else -1
                    for value in legacy_atoms["molecule_index"]
                ],
                dtype=np.int64,
            )
            direct[self.atoms["group_index"].notna().to_numpy()] = -1
            self._atom_molecule_membership = compact(direct)

        if (
            "formal_charge" in legacy_atoms
            and legacy_atoms["formal_charge"].notna().any()
        ):
            self._set_chemical_state_atom_attribute(
                "formal_charge",
                pd.array(legacy_atoms["formal_charge"], dtype="Int16"),
            )
        if (
            "partial_charge" in legacy_atoms
            and legacy_atoms["partial_charge"].notna().any()
        ):
            self._legacy_partial_charge = legacy_atoms["partial_charge"].to_numpy(
                copy=True
            )

        self._coerce_id_columns_to_string()

    def _get_component_indices(self, state_index=None):
        """Return authoritative component membership for a resolved state."""

        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        return state.component_indices

    def _set_component_indices(self, values, atom_indices=None, state_index=None):
        """Set authoritative component membership for a resolved state."""

        if atom_indices is not None and np.asarray(atom_indices).size == 0:
            return
        state = self._resolve_chemical_state(state_index=state_index)
        state._ensure_compatibility(self.n_atoms)
        if atom_indices is None:
            normalized = _ChemicalStateStorage._values_with_length(
                values, self.n_atoms, "component_index"
            )
            normalized = pd.array(normalized, dtype="Int64")
            if (pd.Series(normalized).dropna() < 0).any():
                raise StructuralInconsistencyError(
                    reason="Chemical-state component indices must be non-negative or missing.",
                    caller="molsysmt.native.Topology",
                )
            candidate = pd.Series(normalized, index=range(self.n_atoms))
        else:
            indices = state._normalize_atom_indices(np.atleast_1d(atom_indices))
            normalized = _ChemicalStateStorage._values_with_length(
                values, len(indices), "component_index"
            )
            normalized = pd.array(normalized, dtype="Int64")
            if (pd.Series(normalized).dropna() < 0).any():
                raise StructuralInconsistencyError(
                    reason="Chemical-state component indices must be non-negative or missing.",
                    caller="molsysmt.native.Topology",
                )
            candidate = state.component_indices.copy()
            candidate.loc[indices] = normalized
        with self._invalidating_chemical_interactions():
            state.component_indices = candidate

    def _component_indices_are_missing(self, state_index=None):
        """Return whether any resolved-state component membership is unknown."""

        return self._get_component_indices(state_index=state_index).isnull().any()

    @property
    def chain_groups(self):
        """Getting ordered source group memberships for every native chain.

        Returns an immutable tuple per chain, including empty declared chains.
        Without an explicit declaration, memberships derive from stored atoms.
        A group may belong to multiple chains; no atom or bond is synthesized.
        """
        from ._chain_groups import by_chain

        return tuple(
            tuple(int(index) for index in members) for members in by_chain(self)
        )

    @arg_digest()
    def set_chain_groups(self, chain_groups, skip_digestion=False):
        """Declaring ordered group membership independently of atomic realization.

        Parameters
        ----------
        chain_groups : list, tuple, or None
            One ordered list of unique source group indices per chain. Groups
            can occur in multiple chains. None restores atom-derived membership.
            Declarations must agree with every known atom/group/chain assignment.
        skip_digestion : bool, default=False
            Whether to skip MolSysMT's internal argument digestion mechanism.

        Returns
        -------
        None
            Publish independent compact integer membership after full validation.

        Raises
        ------
        ArgumentError
            If dimensions, integer indices or within-chain uniqueness are invalid.
        StructuralInconsistencyError
            If a declaration contradicts stored atom membership.

        Examples
        --------
        >>> topology = Topology(n_groups=2, n_chains=1)
        >>> topology.set_chain_groups([[1, 0]])
        >>> topology.chain_groups
        ((1, 0),)

        .. admonition:: User guide

           See :ref:`API Native Group Membership` and the Topology foundation
           for declared hierarchy without an atomic realization.

        .. versionadded:: 1.0.0
        """
        from ._chain_groups import pack

        self._chain_group_membership = pack(self, chain_groups)

    @signal(tags=["native"])
    @arg_digest(native_molecule_membership=True)
    def set_atom_molecules(
        self, molecule_indices, atom_indices="all", skip_digestion=False
    ):
        """Declaring stable molecule membership for atoms without groups.

        Parameters
        ----------
        molecule_indices : int, array-like of int or None
            One molecule index per selected atom. None entries declare unknown
            membership. A scalar index assigns one atom; None requests unknown
            ownership for every selected atom. A grouped atom cannot be cleared
            independently of its group. All known indices must identify
            stored molecules. No molecules or groups are created.
        atom_indices : int, array-like of int or 'all', default='all'
            Unique source atom indices, in the assignment order. A grouped
            position must match its group's stored molecule and is a no-op.
        skip_digestion : bool, default=False
            Skip argument digestion only for already validated inputs.

        Returns
        -------
        None
            Publish the validated independent stable membership.

        Raises
        ------
        ArgumentError
            If dimensions or indices are invalid, repeated, boolean or unitful.
        StructuralInconsistencyError
            If a molecule is unavailable, existing membership is misaligned,
            or a declaration conflicts with a group's molecule.

        Notes
        -----
        Molecules and chemical components are independent. Changing a bond,
        component partition or selected chemical state does not change these
        declarations. Grouped atoms continue using their group's molecule.
        Clearing all ungrouped declarations releases the optional vector.

        A supported change invalidates all named interaction analyses in the
        owning MolSys, including evaluated-empty coverage. Old snapshots remain
        intact. Validation and invalidation staging precede publication; failures
        preserve membership and analyses. Coordinates are not copied and no
        detector is run automatically. An unchanged declaration is a no-op.

        Examples
        --------
        >>> topology = Topology(n_atoms=3, n_molecules=2)
        >>> topology.set_atom_molecules([1, 0, None])
        >>> topology.get(element='atom', molecule_index=True)
        [1, 0, None]
        >>> topology.set_atom_molecules(None)
        >>> topology.get(element='atom', molecule_index=True)
        [None, None, None]

        .. admonition:: User guide

           See :ref:`user-foundations-native-world-classes-molsysmt-topology`
           for stable molecule membership and editing.

        .. versionadded:: 1.0.0
        """
        from ._atom_molecules import prepare

        candidate = prepare(self, molecule_indices, atom_indices)
        previous = getattr(self, "_atom_molecule_membership", None)
        if (candidate is None and previous is None) or (
            candidate is not None
            and previous is not None
            and np.array_equal(candidate, previous)
        ):
            return
        owner_ref = getattr(self, "_molsys_owner_ref", None)
        owner = owner_ref() if owner_ref is not None else None
        with (
            owner._invalidating_interaction_frames("all")
            if owner is not None
            else nullcontext()
        ):
            self._atom_molecule_membership = candidate

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

        n_atoms = int(n_atoms)
        if (
            n_atoms != len(getattr(self, "atoms", ()))
            and getattr(self, "_atom_molecule_membership", None) is not None
        ):
            raise StructuralInconsistencyError(
                reason="Resetting atom count would discard declared molecule membership; extract or remove atoms instead."
            )
        if n_atoms != self._chemical_states_domain.n_atoms:
            for state in self._chemical_states:
                if (
                    len(state.bonds)
                    or len(state.components)
                    or state.atom_attributes.shape[1]
                    or state.component_indices.notna().any()
                ):
                    raise StructuralInconsistencyError(
                        reason=(
                            "Resetting the atom count would invalidate chemical-state "
                            "data; extract or remove atoms instead."
                        ),
                        caller="molsysmt.native.Topology.reset_atoms",
                    )
            self._chemical_states_domain._resize_atom_domain(n_atoms)
        self.atoms = Atoms_DataFrame(n_atoms=n_atoms)
        self._atom_molecule_membership = None

    def reset_groups(self, n_groups=0):
        """Reset groups table to a new size."""

        self.groups = Groups_DataFrame(n_groups=n_groups)
        self._chain_group_membership = None

    def reset_components(self, n_components=0):
        """Reset components table to a new size."""

        self.components = Components_DataFrame(n_components=n_components)

    def reset_molecules(self, n_molecules=0):
        """Reset molecules table to a new size."""

        membership = getattr(self, "_atom_molecule_membership", None)
        if membership is not None and np.any(membership >= n_molecules):
            raise StructuralInconsistencyError(
                reason="Resetting molecule count would invalidate declared atom membership."
            )
        self.molecules = Molecules_DataFrame(n_molecules=n_molecules)

    def reset_entities(self, n_entities=0):
        """Reset entities table to a new size."""

        self.entities = Entities_DataFrame(n_entities=n_entities)

    def reset_chains(self, n_chains=0):
        """Reset chains table to a new size."""

        self.chains = Chains_DataFrame(n_chains=n_chains)
        self._chain_group_membership = None

    def reset_bonds(self, n_bonds=0):
        """Reset bonds table to a new size."""

        self._reset_chemical_state_bonds(n_bonds=n_bonds)

    def _coerce_id_columns_to_string(self):
        """Ensure all *_id columns use pandas string dtype."""

        self.atoms["atom_id"] = self.atoms["atom_id"].astype("string")
        self.groups["group_id"] = self.groups["group_id"].astype("string")
        self.components["component_id"] = self.components["component_id"].astype(
            "string"
        )
        self.molecules["molecule_id"] = self.molecules["molecule_id"].astype("string")
        self.entities["entity_id"] = self.entities["entity_id"].astype("string")
        self.chains["chain_id"] = self.chains["chain_id"].astype("string")

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

    @signal(tags=["native"])
    @arg_digest()
    def extract(self, atom_indices="all", copy_if_all=False, skip_digestion=False):
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
            atom_indices = np.sort(np.asarray(atom_indices, dtype=np.int64))

            tmp_item = Topology(skip_digestion=True)
            tmp_item.atoms = self.atoms.iloc[atom_indices].copy()
            tmp_item.atoms.index = pd.RangeIndex(len(tmp_item.atoms))

            old_group_indices = tmp_item.atoms["group_index"].dropna().unique().tolist()
            tmp_item.groups = self.groups.iloc[old_group_indices].copy()
            tmp_item.groups.index = pd.RangeIndex(len(tmp_item.groups))

            from ._atom_molecules import compact, stored

            direct = stored(self)
            old_molecule_indices = (
                tmp_item.groups["molecule_index"].dropna().unique().tolist()
            )
            if direct is not None:
                for molecule in direct[atom_indices]:
                    if molecule >= 0 and int(molecule) not in old_molecule_indices:
                        old_molecule_indices.append(int(molecule))
            tmp_item.molecules = self.molecules.iloc[old_molecule_indices].copy()
            tmp_item.molecules.index = pd.RangeIndex(len(tmp_item.molecules))

            old_entity_indices = (
                tmp_item.molecules["entity_index"].dropna().unique().tolist()
            )
            tmp_item.entities = self.entities.iloc[old_entity_indices].copy()
            tmp_item.entities.index = pd.RangeIndex(len(tmp_item.entities))

            old_chain_indices = tmp_item.atoms["chain_index"].dropna().unique().tolist()
            tmp_item.chains = self.chains.iloc[old_chain_indices].copy()
            tmp_item.chains.index = pd.RangeIndex(len(tmp_item.chains))

            tmp_item.atoms["group_index"] = (
                tmp_item.atoms["group_index"]
                .map({old: new for new, old in enumerate(old_group_indices)})
                .astype("Int64")
            )
            tmp_item.groups["molecule_index"] = (
                tmp_item.groups["molecule_index"]
                .map({old: new for new, old in enumerate(old_molecule_indices)})
                .astype("Int64")
            )
            tmp_item.molecules["entity_index"] = (
                tmp_item.molecules["entity_index"]
                .map({old: new for new, old in enumerate(old_entity_indices)})
                .astype("Int64")
            )
            if direct is not None:
                mapping = {old: new for new, old in enumerate(old_molecule_indices)}
                tmp_item._atom_molecule_membership = compact(
                    np.asarray(
                        [mapping.get(int(value), -1) for value in direct[atom_indices]],
                        dtype=np.int64,
                    )
                )
            tmp_item.atoms["chain_index"] = (
                tmp_item.atoms["chain_index"]
                .map({old: new for new, old in enumerate(old_chain_indices)})
                .astype("Int64")
            )

            tmp_item._chemical_states_domain = (
                self._chemical_states_domain._extract_atoms(atom_indices)
            )
            if self._chain_group_membership is not None:
                from ._chain_groups import by_chain

                membership = by_chain(self)
                group_map = {old: new for new, old in enumerate(old_group_indices)}
                tmp_item.set_chain_groups(
                    [
                        [
                            group_map[int(g)]
                            for g in membership[chain]
                            if int(g) in group_map
                        ]
                        for chain in old_chain_indices
                    ]
                )
            tmp_item.atoms["atom_id"] = tmp_item.atoms["atom_id"].astype("string")
            tmp_item.groups["group_id"] = tmp_item.groups["group_id"].astype("string")
            tmp_item.molecules["molecule_id"] = tmp_item.molecules[
                "molecule_id"
            ].astype("string")
            tmp_item.entities["entity_id"] = tmp_item.entities["entity_id"].astype(
                "string"
            )
            tmp_item.chains["chain_id"] = tmp_item.chains["chain_id"].astype("string")
            for chemical_state in tmp_item._chemical_states:
                chemical_state.components["component_id"] = chemical_state.components[
                    "component_id"
                ].astype("string")
            return tmp_item

    @signal(tags=["native"])
    @arg_digest()
    def remove(self, atom_indices=None, copy_if_None=False, skip_digestion=False):
        """Remove atoms by index and return the resulting topology."""

        if atom_indices is None:
            if copy_if_None:
                return self.copy()
            else:
                return self

        else:
            atom_indices_to_be_kept = np.setdiff1d(
                np.arange(self.n_atoms), atom_indices
            )

            tmp_item = self.extract(
                atom_indices=atom_indices_to_be_kept, skip_digestion=True
            )

            return tmp_item

    @signal(tags=["native"])
    @arg_digest(form="molsysmt.Topology")
    def add(self, item, atom_indices="all", keep_ids=True, skip_digestion=False):
        """Appending another topology, offsetting indices as needed.

        Chain indices are offset independently of their labels. Explicit chain
        IDs and names are preserved when ``keep_ids=True``, including duplicate
        IDs; ``keep_ids=False`` regenerates local IDs.
        Native public calls validate the boolean ``keep_ids`` argument; leave
        ``skip_digestion=False`` for ordinary calls.
        """

        if len(self._chemical_states) != 1 or len(item._chemical_states) != 1:
            raise StructuralInconsistencyError(
                reason=(
                    "Adding topologies with multiple or absent chemical states requires an explicit "
                    "state-alignment policy and is not inferred automatically."
                ),
                caller="molsysmt.native.Topology.add",
            )

        if is_all(atom_indices):
            tmp_item = item.copy()
        else:
            tmp_item = item.extract(atom_indices=atom_indices, skip_digestion=True)

        from ._chain_groups import by_chain

        declared = (
            self._chain_group_membership is not None
            or tmp_item._chain_group_membership is not None
        )
        membership = None
        if declared:
            membership = [groups.tolist() for groups in by_chain(self)] + [
                (groups + self.n_groups).tolist() for groups in by_chain(tmp_item)
            ]
            tmp_item.molecules["entity_index"] += self.n_entities
            entities = pd.concat([self.entities, tmp_item.entities], ignore_index=True)

        n_atoms = self.atoms.shape[0]
        n_groups = self.groups.shape[0]
        n_components = self.components.shape[0]
        n_molecules = self.molecules.shape[0]
        n_chains = self.chains.shape[0]

        from ._atom_molecules import compact, stored

        own_membership, other_membership = stored(self), stored(tmp_item)
        combined_membership = None
        if own_membership is not None or other_membership is not None:
            left = (
                np.full(n_atoms, -1, dtype=np.int64)
                if own_membership is None
                else own_membership
            )
            right = (
                np.full(tmp_item.n_atoms, -1, dtype=np.int64)
                if other_membership is None
                else other_membership.copy()
            )
            right[right >= 0] += n_molecules
            combined_membership = compact(np.concatenate([left, right]))

        tmp_item.atoms["group_index"] += n_groups
        tmp_item._set_component_indices(
            tmp_item._get_component_indices() + n_components
        )
        tmp_item.atoms["chain_index"] += n_chains
        tmp_item.groups["molecule_index"] += n_molecules
        combined_component_indices = pd.concat(
            [self._get_component_indices(), tmp_item._get_component_indices()],
            ignore_index=True,
        ).astype("Int64")
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

        self.atoms = pd.concat([self.atoms, tmp_item.atoms], ignore_index=True)
        self._chemical_states_domain._n_atoms = len(self.atoms)
        self._reference_chemical_state.component_indices = combined_component_indices
        self._reference_chemical_state.atom_attributes = combined_atom_attributes
        self._reference_chemical_state._normalize_atom_attribute_columns()
        self.groups = pd.concat([self.groups, tmp_item.groups], ignore_index=True)
        self.molecules = pd.concat(
            [self.molecules, tmp_item.molecules], ignore_index=True
        )
        self._atom_molecule_membership = combined_membership
        self.components = pd.concat(
            [self.components, tmp_item.components], ignore_index=True
        )
        self.chains = pd.concat([self.chains, tmp_item.chains], ignore_index=True)
        combined_bonds = self._concatenate_bond_tables(
            self._get_chemical_state_bonds(), tmp_bonds
        )
        self._set_chemical_state_bonds(combined_bonds)
        from copy import deepcopy

        self._reference_chemical_state._preparation_history.extend(
            deepcopy(tmp_item._reference_chemical_state._preparation_history)
        )

        if declared:
            self.entities = entities
            self.set_chain_groups(membership)
            if not keep_ids:
                from ._topology_infer import fallback_ids, infer_chain_ids_from_topology

                for plural, singular in (
                    ("atoms", "atom"),
                    ("groups", "group"),
                    ("molecules", "molecule"),
                    ("entities", "entity"),
                ):
                    table = getattr(self, plural)
                    table[singular + "_id"] = fallback_ids(len(table))
                self.chains["chain_id"] = infer_chain_ids_from_topology(self)
            if self.n_atoms:
                self.rebuild_components(
                    redefine_indices=True,
                    redefine_ids=not keep_ids,
                    redefine_names=True,
                    redefine_types=True,
                )
            self._coerce_id_columns_to_string()
            return

        if not keep_ids:
            self.rebuild_atoms(redefine_ids=True, redefine_types=False)
            self.rebuild_groups(redefine_ids=True, redefine_types=False)

        self.rebuild_components(
            redefine_indices=True,
            redefine_ids=(not keep_ids),
            redefine_names=True,
            redefine_types=True,
        )
        self.rebuild_chains(
            redefine_indices=False,
            redefine_ids=(not keep_ids),
            redefine_types=True,
            redefine_names=False,
        )

        self.rebuild_molecules(
            redefine_indices=False,
            redefine_ids=(not keep_ids),
            redefine_types=False,
            redefine_names=True,
        )
        self.rebuild_entities(
            redefine_indices=True,
            redefine_ids=True,
            redefine_names=True,
            redefine_types=True,
        )
        self._coerce_id_columns_to_string()
        del tmp_item

    @signal(tags=["native"])
    @arg_digest()
    def copy(self, *, skip_digestion=False):
        """Copying canonical topology tables and chemistry independently.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        Topology
            An independent topology preserving the concrete native type.

        Notes
        -----
        Canonical tables and mutable metadata are copied eagerly. The source
        MolSys weak owner is excluded; a separately copied topology can be
        attached to another system. Copying preserves stored IDs, chemical
        states, dirty flags and extension state without inference or migration.
        Owner exclusion also applies to extension slots. Other slots retain
        distinct declaring-class storage and shared-memo aliases. Arbitrary
        mutable table-cell values and pandas metadata follow pandas' copy rules.

        Examples
        --------
        >>> topology = Topology(n_atoms=2)
        >>> duplicate = topology.copy()
        >>> duplicate is topology
        False
        >>> duplicate.n_atoms
        2

        .. admonition:: User guide

           See :ref:`user-foundations-resident-copying` for native and payload copy contracts.

        .. versionadded:: 1.0.0
        """
        from ._copy import _copy_independently

        return _copy_independently(self, skip_digestion)

    @signal(tags=["native"])
    @arg_digest(native_topology_bonds=True)
    def add_bonds(self, bonded_atom_pairs, skip_digestion=False):
        """Adding covalent edges and rebuilding their connected components.

        Parameters
        ----------
        bonded_atom_pairs : array-like of int
            Atom-index pairs with shape (n_bonds, 2), within this topology's
            atom domain. Self-edges and duplicate unordered pairs are rejected.
            An empty sequence changes nothing.
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        None
            Bonds and component assignments are updated in the resolved state.

        Raises
        ------
        ArgumentError
            If pairs are malformed or do not contain integer indices.
        StructuralInconsistencyError
            If endpoints are out of range, self-edges or duplicate edges.

        Notes
        -----
        An attached topology notifies its owning MolSys before publishing bonds:
        every named analysis becomes unevaluated, including evaluated-empty
        structures. No detector runs automatically. Invalid input or failure to
        stage invalidation preserves the bond table and analyses. A subsequent
        component-rebuilding failure can leave the new bonds published, with
        analyses already invalidated. Standalone copies have no owner link.

        Examples
        --------
        >>> topology = Topology(n_atoms=3)
        >>> topology.add_bonds([[0, 1]])
        >>> topology.n_bonds
        1

        .. admonition:: User guide

           See :ref:`user-foundations-native-world-classes-molsysmt-topology`.

        .. versionadded:: 1.0.0
        """

        if np.asarray(bonded_atom_pairs).size == 0:
            return
        self._append_chemical_state_bonds(bonded_atom_pairs)

        self.rebuild_components(
            redefine_indices=True,
            redefine_ids=True,
            redefine_names=True,
            redefine_types=True,
        )

    @arg_digest(native_topology_bonds=True)
    def remove_bonds(self, bond_indices="all", skip_digestion=False):
        """Removing covalent edges and rebuilding their connected components.

        Parameters
        ----------
        bond_indices : int or array-like of int or str, default='all'
            Positional bond indices to remove; 'all' removes every bond. An
            empty sequence changes nothing. Remaining indices are compacted.
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        None
            Bonds and component assignments are updated in the resolved state.

        Raises
        ------
        ArgumentError
            If indices are not integers or a one-dimensional sequence.
        KeyError
            If a requested bond index is unavailable.

        Notes
        -----
        An attached topology invalidates every named analysis in its MolSys
        before publishing changed bonds. This includes evaluated-empty coverage;
        earlier result/query snapshots survive. Invalid input and invalidation
        allocation failure preserve the original table and analyses. Component
        rebuilding follows publication and can fail after the chemical edit;
        analyses remain invalidated. No detector runs automatically.

        Examples
        --------
        >>> topology = Topology(n_atoms=3)
        >>> topology.add_bonds([[0, 1], [1, 2]])
        >>> topology.remove_bonds([0])
        >>> topology.n_bonds
        1

        .. admonition:: User guide

           See :ref:`user-foundations-native-world-classes-molsysmt-topology`.

        .. versionadded:: 1.0.0
        """

        if not is_all(bond_indices) and np.asarray(bond_indices).size == 0:
            return
        if is_all(bond_indices) and not self.n_bonds:
            return
        self._remove_chemical_state_bonds(bond_indices=bond_indices)

        self.rebuild_components(
            redefine_indices=True,
            redefine_ids=True,
            redefine_names=True,
            redefine_types=True,
        )

    def add_missing_bonds(
        self, selection="all", syntax="MolSysMT", skip_digestion=False
    ):
        """Infer and add missing bonds using geometric templates."""

        from molsysmt.build import get_missing_bonds as _get_missing_bonds

        bonds = _get_missing_bonds(
            self,
            selection=selection,
            syntax=syntax,
            engine="MolSysMT",
            with_templates=True,
            with_distances=False,
            skip_digestion=True,
        )

        self.add_bonds(bonds, skip_digestion=True)

        self.rebuild_components(
            redefine_indices=True,
            redefine_ids=False,
            redefine_names=False,
            redefine_types=False,
        )

    def rebuild_atoms(self, redefine_ids=True, redefine_types=True):
        """Regenerate atom ids/types from names and current counts."""

        if redefine_ids:
            self.atoms["atom_id"] = np.arange(self.atoms.shape[0], dtype=int).astype(
                str
            )

        if redefine_types:
            from molsysmt.element.atom import get_atom_type_from_atom_name

            aux_dict = {}

            atom_types = []

            for atom_name in self.atoms["atom_name"].values:
                if atom_name not in aux_dict:
                    atom_type = get_atom_type_from_atom_name(atom_name)
                    aux_dict[atom_name] = atom_type
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
            self.groups["group_id"] = np.arange(self.groups.shape[0], dtype=int).astype(
                str
            )

        if redefine_types:
            from ._topology_infer import infer_group_types_from_topology

            self.groups.group_type = infer_group_types_from_topology(self)
        self._coerce_id_columns_to_string()

    @signal(tags=["native"])
    def rebuild_components(
        self,
        redefine_indices=True,
        redefine_ids=True,
        redefine_types=True,
        redefine_names=True,
        force=False,
    ):
        """Rebuilding native component membership and metadata from local evidence.

        Parameters
        ----------
        redefine_indices : bool
            Recompute atom-level component indices from stored connectivity.
            Default True.
        redefine_ids : bool
            Generate local string IDs. If False, retain IDs only for components
            whose atom membership is unchanged by index reconstruction. Default True.
        redefine_types : bool
            Infer types from native group data. If False, retain types only for
            components whose atom membership is unchanged. Default True.
        redefine_names : bool
            Infer names from native group data. If False, retain names only for
            components whose atom membership is unchanged. Default True.
        force : bool
            Reconstruct component indices even if redefine_indices is False.
            Default False.

        Returns
        -------
        None
            Update the resolved chemical state's component tables in place.

        Notes
        -----
        Component indices are inferred from connectivity. Component ids are
        synthesized as stable local string ids when requested. Component types
        and names are inferred from the current native group/component content.
        Matching unchanged components uses exact atom-set equality, independently
        of component row numbers. Merged or split components have unknown metadata
        unless the corresponding redefinition is requested. No connectivity
        completeness claim follows from preserving labels.
        This method is a native API and is not form-agnostic.

        Examples
        --------
        >>> topology = Topology(n_atoms=1)
        >>> topology.rebuild_components()
        >>> topology.components["component_id"] = ["ion"]
        >>> topology.rebuild_components(redefine_ids=False, redefine_types=False, redefine_names=False)
        >>> topology.components.component_id.tolist()
        ['ion']
        """
        from ._topology_infer import (
            _needs_columns,
            _unchanged_component_rows,
            fallback_ids,
            infer_component_indices_from_topology,
            infer_component_names_from_topology,
            infer_component_types_from_topology,
        )

        if redefine_types and _needs_columns(self.groups, ["group_type"]):
            self.rebuild_groups(redefine_ids=False, redefine_types=True)

        need_component_indices = (
            redefine_names or redefine_types
        ) and self._component_indices_are_missing()

        if redefine_indices or force or need_component_indices:
            preserved_columns = [
                column
                for column, redefine in (
                    ("component_id", redefine_ids),
                    ("component_type", redefine_types),
                    ("component_name", redefine_names),
                )
                if not redefine
            ]
            old_components = self.components if preserved_columns else None
            old_indices = (
                self._get_component_indices().to_numpy(dtype=np.int64, na_value=-1)
                if preserved_columns
                else None
            )
            component_index_of_atoms = infer_component_indices_from_topology(self)
            self._set_component_indices(component_index_of_atoms)

            if len(component_index_of_atoms) > 0:
                n_components = int(np.max(component_index_of_atoms)) + 1
            else:
                n_components = 0
            self.components = Components_DataFrame(n_components=n_components)
            if preserved_columns:
                new_rows, old_rows = _unchanged_component_rows(
                    old_indices,
                    component_index_of_atoms,
                    len(old_components),
                    n_components,
                )
                for column in preserved_columns:
                    # Missing labels must not become the legacy string "nan".
                    self.components[column] = np.full(n_components, pd.NA, dtype=object)
                    self.components.loc[new_rows, column] = (
                        old_components[column].iloc[old_rows].to_numpy()
                    )

            del component_index_of_atoms

        if redefine_ids:
            self.components["component_id"] = fallback_ids(self.n_components)

        if redefine_types:
            self.components["component_type"] = infer_component_types_from_topology(
                self
            )

        if redefine_names:
            self.components["component_name"] = infer_component_names_from_topology(
                self
            )

        state = self._resolve_chemical_state()
        state.component_evidence = "inferred"
        bonds = state.bonds
        participation_complete = (
            "joins_components" in bonds.columns
            and not bonds["joins_components"].isna().any()
        )
        if state.connectivity_completeness == "complete" and participation_complete:
            state.component_completeness = "complete"
        else:
            state.component_completeness = "partial"

        self._components_dirty = False
        if redefine_indices or force:
            self._molecules_dirty = True

        self._coerce_id_columns_to_string()

    @signal(tags=["native"])
    def rebuild_molecules(
        self,
        redefine_indices=True,
        redefine_ids=True,
        redefine_names=True,
        redefine_types=True,
        molecules_as_components=True,
        force=False,
    ):
        """Rebuilding native molecule membership and metadata from local evidence.

        Notes
        -----
        When no better molecule definition is available, molecules fall back to
        components. Under that fallback, molecule name and type inherit from the
        corresponding component. Atom-free group inventories retain declared
        molecule slots, including empty occurrences, and fill only missing owners
        from the represented group/chain hierarchy. No atomic connectivity is
        inferred for these inventories. An inventory without groups uses the reference
        component partition directly, retaining zero groups. Other chemical
        states do not silently redefine this fallback molecular axis. This
        method is a native API and is not form-agnostic.
        """
        from ._topology_infer import (
            _needs_columns,
            fallback_ids,
            infer_molecule_indices_from_topology,
            infer_molecule_names_from_topology,
            infer_molecule_types_from_topology,
        )

        if (
            self.n_groups == 0
            and getattr(self, "_atom_molecule_membership", None) is not None
        ):
            if redefine_ids:
                self.molecules["molecule_id"] = fallback_ids(self.n_molecules)
            if redefine_types:
                self.molecules["molecule_type"] = infer_molecule_types_from_topology(
                    self
                )
            if redefine_names:
                self.molecules["molecule_name"] = infer_molecule_names_from_topology(
                    self
                )
            self._molecules_dirty = False
            return

        need_component_types = (redefine_names or redefine_types) and _needs_columns(
            self.components, ["component_type"]
        )
        need_component_names = redefine_names and _needs_columns(
            self.components, ["component_name"]
        )
        need_component_indices = (
            redefine_names or redefine_types or redefine_indices
        ) and self._component_indices_are_missing()
        if self.n_atoms and (
            need_component_indices or need_component_types or need_component_names
        ):
            self.rebuild_components(
                redefine_indices=need_component_indices,
                redefine_ids=False,
                redefine_types=(
                    redefine_types or need_component_types or need_component_names
                ),
                redefine_names=(redefine_names or need_component_names),
                force=need_component_indices,
            )

        need_molecule_indices = (redefine_names or redefine_types) and _needs_columns(
            self.groups, ["molecule_index"]
        )

        if self.n_atoms == 0:
            from ._topology_infer import complete_missing_molecule_membership

            complete_missing_molecule_membership(self)
        elif redefine_indices or force or need_molecule_indices:
            molecule_index_of_groups = infer_molecule_indices_from_topology(self)
            self.groups["molecule_index"] = molecule_index_of_groups.astype(int)
            if len(molecule_index_of_groups) > 0:
                n_molecules = int(np.max(molecule_index_of_groups)) + 1
            else:
                n_molecules = len(self._resolve_reference_chemical_state().components)
            self.reset_molecules(n_molecules=n_molecules)
            if self.n_groups == 0:
                # Initial explicit hierarchy construction snapshots the selected
                # reference partition; subsequent stable queries never read it.
                state = self._resolve_reference_chemical_state()
                self.molecules["molecule_name"] = state.components[
                    "component_name"
                ].to_numpy(copy=True)
                self.molecules["molecule_type"] = state.components[
                    "component_type"
                ].to_numpy(copy=True)
                self.set_atom_molecules(
                    state.component_indices.to_numpy(dtype=np.int64),
                    skip_digestion=True,
                )

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

    @signal(tags=["native"])
    def rebuild_chains(
        self,
        redefine_indices=True,
        redefine_ids=True,
        redefine_types=True,
        redefine_names=True,
    ):
        """Rebuilding native chain membership and metadata from local evidence.

        Notes
        -----
        Chain indices are rebuilt from the current native atom/group assignment.
        An explicit chain/group relation and empty chain declarations are retained.
        Generated IDs follow A through Z, then AA, AB and onward. Chain ids and names are regenerated as stable local values when
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

        need_molecule_types = redefine_types and _needs_columns(
            self.molecules, ["molecule_type"]
        )
        if need_molecule_types:
            self.rebuild_molecules(
                redefine_indices=False,
                redefine_ids=False,
                redefine_names=False,
                redefine_types=True,
            )

        need_chain_indices = (redefine_names or redefine_types) and _needs_columns(
            self.atoms, ["chain_index"]
        )

        if (redefine_indices or need_chain_indices) and not (
            self.n_atoms == 0 or self._chain_group_membership is not None
        ):
            chain_index_of_atoms = infer_chain_indices_from_topology(self)
            self.atoms["chain_index"] = np.array(chain_index_of_atoms, dtype=int)

            if len(chain_index_of_atoms) > 0:
                n_chains = int(np.max(chain_index_of_atoms)) + 1
            else:
                n_chains = 0
            self.reset_chains(n_chains=n_chains)

            del chain_index_of_atoms

        if redefine_ids:
            self.chains["chain_id"] = infer_chain_ids_from_topology(self)

        if redefine_types:
            self.chains["chain_type"] = infer_chain_types_from_topology(self)

        if redefine_names:
            self.chains["chain_name"] = infer_chain_names_from_topology(self)

        self._chains_dirty = False

        self._coerce_id_columns_to_string()

    @signal(tags=["native"])
    def rebuild_entities(
        self,
        redefine_indices=True,
        redefine_ids=True,
        redefine_names=True,
        redefine_types=True,
        force=False,
    ):
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

        need_molecule_names = redefine_names and _needs_columns(
            self.molecules, ["molecule_name"]
        )
        need_molecule_types = redefine_types and _needs_columns(
            self.molecules, ["molecule_type"]
        )
        need_entity_indices = (redefine_names or redefine_types) and _needs_columns(
            self.molecules, ["entity_index"]
        )
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
            self.reset_entities(n_entities=n_entities)

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
    def compare(
        self, item, rule="equal", output_type="boolean", skip_digestion=False, **kwargs
    ):
        """Compare topology content with another topology."""

        if rule == "equal":
            output = {}

            if "n_atoms" in kwargs:
                tmp_output = self.atoms.shape[0] == item.atoms.shape[0]
                output["n_atoms"] = kwargs["n_atoms"] == tmp_output

            if "atom_index" in kwargs:
                tmp_output = self.atoms.shape[0] == item.atoms.shape[0]
                output["atom_index"] = kwargs["atom_index"] == tmp_output

            if "atom_id" in kwargs:
                tmp_output = (
                    self.atoms["atom_id"].values == item.atoms["atom_id"].values
                ).all()
                output["atom_id"] = kwargs["atom_id"] == tmp_output

            if "atom_name" in kwargs:
                tmp_output = (
                    self.atoms["atom_name"].values == item.atoms["atom_name"].values
                ).all()
                output["atom_name"] = kwargs["atom_name"] == tmp_output

            if "atom_type" in kwargs:
                tmp_output = (
                    self.atoms["atom_type"].values == item.atoms["atom_type"].values
                ).all()
                output["atom_type"] = kwargs["atom_type"] == tmp_output

            if "n_groups" in kwargs:
                tmp_output = self.groups.shape[0] == item.groups.shape[0]
                output["n_groups"] = kwargs["n_groups"] == tmp_output

            if "group_index" in kwargs:
                tmp_output = (
                    self.atoms["group_index"].values == item.atoms["group_index"].values
                ).all()
                output["group_index"] = kwargs["group_index"] == tmp_output

            if "group_id" in kwargs:
                tmp_output = (
                    self.groups["group_id"].values == item.groups["group_id"].values
                ).all()
                output["group_id"] = kwargs["group_id"] == tmp_output

            if "group_name" in kwargs:
                tmp_output = (
                    self.groups["group_name"].values == item.groups["group_name"].values
                ).all()
                output["group_name"] = kwargs["group_name"] == tmp_output

            if "group_type" in kwargs:
                tmp_output = (
                    self.groups["group_type"].values == item.groups["group_type"].values
                ).all()
                output["group_type"] = kwargs["group_type"] == tmp_output

            if "component_index" in kwargs:
                tmp_output = (
                    self._get_component_indices().values
                    == item._get_component_indices().values
                ).all()
                output["component_index"] = kwargs["component_index"] == tmp_output

            if "component_id" in kwargs:
                tmp_output = (
                    self.components["component_id"].values
                    == item.components["component_id"].values
                ).all()
                output["component_id"] = kwargs["component_id"] == tmp_output

            if "component_name" in kwargs:
                tmp_output = (
                    self.components["component_name"].values
                    == item.components["component_name"].values
                ).all()
                output["component_name"] = kwargs["component_name"] == tmp_output

            if "component_type" in kwargs:
                tmp_output = (
                    self.components["component_type"].values
                    == item.components["component_type"].values
                ).all()
                output["component_type"] = kwargs["component_type"] == tmp_output

            if "molecule_index" in kwargs:
                from ._atom_molecules import resolve

                tmp_output = self.groups["molecule_index"].equals(
                    item.groups["molecule_index"]
                ) and np.array_equal(resolve(self), resolve(item))
                output["molecule_index"] = kwargs["molecule_index"] == tmp_output

            if "molecule_id" in kwargs:
                tmp_output = (
                    self.molecules["molecule_id"].values
                    == item.molecules["molecule_id"].values
                ).all()
                output["molecule_id"] = kwargs["molecule_id"] == tmp_output

            if "molecule_name" in kwargs:
                tmp_output = (
                    self.molecules["molecule_name"].values
                    == item.molecules["molecule_name"].values
                ).all()
                output["molecule_name"] = kwargs["molecule_name"] == tmp_output

            if "molecule_type" in kwargs:
                tmp_output = (
                    self.molecules["molecule_type"].values
                    == item.molecules["molecule_type"].values
                ).all()
                output["molecule_type"] = kwargs["molecule_type"] == tmp_output

            if "entity_index" in kwargs:
                tmp_output = (
                    self.molecules["entity_index"].values
                    == item.molecules["entity_index"].values
                ).all()
                output["entity_index"] = kwargs["entity_index"] == tmp_output

            if "entity_id" in kwargs:
                tmp_output = (
                    self.entities["entity_id"].values
                    == item.entities["entity_id"].values
                ).all()
                output["entity_id"] = kwargs["entity_id"] == tmp_output

            if "entity_name" in kwargs:
                tmp_output = (
                    self.entities["entity_name"].values
                    == item.entities["entity_name"].values
                ).all()
                output["entity_name"] = kwargs["entity_name"] == tmp_output

            if "entity_type" in kwargs:
                tmp_output = (
                    self.entities["entity_type"].values
                    == item.entities["entity_type"].values
                ).all()
                output["entity_type"] = kwargs["entity_type"] == tmp_output

            if "chain_index" in kwargs:
                tmp_output = (
                    self.atoms["chain_index"].values == item.atoms["chain_index"].values
                ).all()
                output["chain_index"] = kwargs["chain_index"] == tmp_output

            if "chain_id" in kwargs:
                tmp_output = (
                    self.chains["chain_id"].values == item.chains["chain_id"].values
                ).all()
                output["chain_id"] = kwargs["chain_id"] == tmp_output

            if "chain_name" in kwargs:
                tmp_output = (
                    self.chains["chain_name"].values == item.chains["chain_name"].values
                ).all()
                output["chain_name"] = kwargs["chain_name"] == tmp_output

            if "chain_type" in kwargs:
                tmp_output = (
                    self.chains["chain_type"].values == item.chains["chain_type"].values
                ).all()
                output["chain_type"] = kwargs["chain_type"] == tmp_output

            if "n_bonds" in kwargs:
                tmp_output = (
                    self._get_chemical_state_bonds().shape[0]
                    == item._get_chemical_state_bonds().shape[0]
                )
                output["n_bonds"] = kwargs["n_bonds"] == tmp_output

            if "bonded_atom_pairs" in kwargs:
                bonds = self._get_chemical_state_bonds()
                item_bonds = item._get_chemical_state_bonds()
                tmp_output1 = (bonds["atom1_index"] == item_bonds["atom1_index"]).all()
                tmp_output2 = (bonds["atom2_index"] == item_bonds["atom2_index"]).all()
                tmp_output = tmp_output1 * tmp_output2
                output["bonded_atom_pairs"] = kwargs["bonded_atom_pairs"] == tmp_output

        if output_type == "boolean":
            output = all(list(output.values()))

        return output

    def get_atom_indices(self, **kwargs):
        """Select atom indices matching the provided hierarchical filters."""

        for aux in kwargs:
            if isinstance(kwargs[aux], (str, int)):
                kwargs[aux] = [kwargs[aux]]
            if aux.endswith("_id") and kwargs[aux] is not None:
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
            if "entity_index" not in molecule_columns:
                molecule_columns.append("entity_index")

        if len(molecule_columns):
            if "molecule_index" not in group_columns:
                group_columns.append("molecule_index")

        if len(group_columns):
            if "group_index" not in atom_columns:
                atom_columns.append("group_index")

        if len(component_columns):
            if "component_index" not in atom_columns:
                atom_columns.append("component_index")

        if len(chain_columns):
            if "chain_index" not in atom_columns:
                atom_columns.append("chain_index")

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
