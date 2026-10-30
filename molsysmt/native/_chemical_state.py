"""Own typed chemical-state storage independently of stable topology.

ChemicalStates owns these records, scientific validation and diagnostic
identities. Stable Topology does not own or reconstruct chemical records.
"""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError


class Components_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing component-level fields."""

    def __init__(self, n_components=0):
        """Initialize a components table with default types."""

        columns = ["component_id", "component_name", "component_type"]

        super().__init__(index=range(n_components), columns=columns)

        self["component_id"] = self["component_id"].astype("string")
        self["component_name"] = self["component_name"].astype(str)
        self["component_type"] = self["component_type"].astype(str)

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column] = self[column].fillna(pd.NA)
        self["component_id"] = self["component_id"].astype("string")


_BOND_REQUIRED_COLUMNS = ("atom1_index", "atom2_index")
_BOND_OPTIONAL_DTYPES = {
    "bond_id": "string",
    "bond_order": "UInt8",
    "fractional_bond_order": "Float64",
    "bond_type": "string",
    "is_aromatic": "boolean",
    "is_conjugated": "boolean",
    "stereochemistry": "string",
    "stereo_atom1_index": "Int64",
    "stereo_atom2_index": "Int64",
    "donor_atom_index": "Int64",
    "acceptor_atom_index": "Int64",
    "joins_components": "boolean",
    "evidence": "string",
    "provenance_index": "Int64",
}
_BOND_ALLOWED_COLUMNS = frozenset(_BOND_REQUIRED_COLUMNS) | frozenset(
    _BOND_OPTIONAL_DTYPES
)
_BOND_ATOM_REFERENCE_COLUMNS = (
    "atom1_index",
    "atom2_index",
    "stereo_atom1_index",
    "stereo_atom2_index",
    "donor_atom_index",
    "acceptor_atom_index",
)


class Bonds_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing normalized chemical-state bonds."""

    def __init__(self, n_bonds=0):
        """Initialize a bonds table with default types."""

        super().__init__(index=range(n_bonds), columns=list(_BOND_REQUIRED_COLUMNS))

        self["atom1_index"] = self["atom1_index"].astype("Int64")
        self["atom2_index"] = self["atom2_index"].astype("Int64")

    def __setitem__(self, key, value):
        if isinstance(key, str) and key not in _BOND_ALLOWED_COLUMNS:
            raise AttributeError(
                f"Bonds_DataFrame has no canonical column {key!r}. "
                f"Allowed columns: {sorted(_BOND_ALLOWED_COLUMNS)}."
            )
        super().__setitem__(key, value)
        if isinstance(key, str):
            dtype = (
                "Int64" if key in _BOND_REQUIRED_COLUMNS else _BOND_OPTIONAL_DTYPES[key]
            )
            super().__setitem__(key, pd.array(self[key], dtype=dtype))

    def _reset(self, n_bonds=0):
        """Rebuild the bonds table to a clean state with the given size."""

        super().__init__(index=range(n_bonds), columns=list(_BOND_REQUIRED_COLUMNS))

        self["atom1_index"] = self["atom1_index"].astype("Int64")
        self["atom2_index"] = self["atom2_index"].astype("Int64")

    def _fix_null_values(self):
        """Normalize missing values in optional bond columns."""

        self["atom1_index"] = pd.array(self["atom1_index"], dtype="Int64")
        self["atom2_index"] = pd.array(self["atom2_index"], dtype="Int64")
        for column, dtype in _BOND_OPTIONAL_DTYPES.items():
            if column in self.columns:
                self[column] = pd.array(self[column], dtype=dtype)

    def _sort_bonds(self):
        """Sort bonds so `atom1_index` is always <= `atom2_index`."""

        mask = self["atom1_index"] > self["atom2_index"]
        self.loc[mask, ["atom1_index", "atom2_index"]] = self.loc[
            mask, ["atom2_index", "atom1_index"]
        ].values
        ordered = self.sort_values(by=["atom1_index", "atom2_index"], ignore_index=True)
        # Keep the authoritative table object and nullable column dtypes. Array
        # assignment is positional even when the old index has arbitrary labels.
        self.index = ordered.index
        for column in self.columns:
            self[column] = ordered[column].array.copy()

    def _remove_empty_columns(self):
        """Drop optional columns when they only contain NaN placeholders."""

        for column in _BOND_OPTIONAL_DTYPES:
            if column in self.columns:
                if self[column].isna().all():
                    del self[column]


_CHEMICAL_STATE_COMPLETENESS_VALUES = frozenset({"unavailable", "partial", "complete"})
_CHEMICAL_STATE_EVIDENCE_VALUES = frozenset(
    {"explicit", "inferred", "user_defined", "unknown"}
)
_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES = {
    "formal_charge": "Int16",
    "is_aromatic": "boolean",
    "n_unpaired_electrons": "UInt8",
    "n_implicit_hydrogens": "UInt8",
    "n_explicit_hydrogens": "UInt8",
    "allows_implicit_hydrogens": "boolean",
    "stereochemistry": "string",
}
_CHEMICAL_STATE_ATOM_STEREOCHEMISTRY_VALUES = frozenset(
    {"R", "S", "r", "s", "unspecified", "unknown"}
)


class _ChemicalStateStorage:
    """Store the private data owned by one chemical state.

    Optional atom-state columns are materialized only when assigned. Component
    membership is an always-aligned nullable vector because it is the link to
    the state-local component table, not stable topology inventory.
    """

    def __init__(
        self,
        n_atoms=0,
        bonds=None,
        components=None,
        component_indices=None,
        state_id=None,
        connectivity_completeness="unavailable",
        component_completeness="unavailable",
        component_evidence="unknown",
        provenance_index=None,
        preparation_history=None,
    ):
        self.state_id = None if state_id is None else str(state_id)
        self.atom_attributes = pd.DataFrame(index=range(n_atoms))
        if component_indices is None:
            component_indices = [pd.NA] * n_atoms
        self.component_indices = pd.Series(
            pd.array(component_indices, dtype="Int64"), index=range(n_atoms)
        )
        self.bonds = Bonds_DataFrame(n_bonds=0) if bonds is None else bonds
        self.components = (
            Components_DataFrame(n_components=0) if components is None else components
        )
        self.connectivity_completeness = connectivity_completeness
        self.component_completeness = component_completeness
        self.component_evidence = component_evidence
        self.provenance_index = provenance_index
        from copy import deepcopy

        from molsysmt._private.preparation_history import validate_history

        history = [] if preparation_history is None else preparation_history
        validate_history(history)
        self._preparation_history = deepcopy(list(history))

    @staticmethod
    def _validate_choice(field, value, choices):
        if value not in choices:
            raise StructuralInconsistencyError(
                reason=f"Invalid chemical-state {field} {value!r}; expected one of {sorted(choices)}.",
                caller="molsysmt.native.topology._ChemicalStateStorage",
            )
        return value

    @property
    def connectivity_completeness(self):
        return self._connectivity_completeness

    @connectivity_completeness.setter
    def connectivity_completeness(self, value):
        self._connectivity_completeness = self._validate_choice(
            "connectivity completeness", value, _CHEMICAL_STATE_COMPLETENESS_VALUES
        )

    @property
    def component_completeness(self):
        return self._component_completeness

    @component_completeness.setter
    def component_completeness(self, value):
        self._component_completeness = self._validate_choice(
            "component completeness", value, _CHEMICAL_STATE_COMPLETENESS_VALUES
        )

    @property
    def component_evidence(self):
        return self._component_evidence

    @component_evidence.setter
    def component_evidence(self, value):
        self._component_evidence = self._validate_choice(
            "component evidence", value, _CHEMICAL_STATE_EVIDENCE_VALUES
        )

    @property
    def provenance_index(self):
        return self._provenance_index

    @provenance_index.setter
    def provenance_index(self, value):
        if value is not None:
            if not isinstance(value, (int, np.integer)) or value < 0:
                raise StructuralInconsistencyError(
                    reason="Chemical-state provenance_index must be a non-negative integer or None.",
                    caller="molsysmt.native.topology._ChemicalStateStorage",
                )
            value = int(value)
        self._provenance_index = value

    def _ensure_compatibility(self, n_atoms):
        """Fill metadata absent from storage created by an older MolSysMT."""

        if not hasattr(self, "state_id"):
            self.state_id = None
        if not hasattr(self, "atom_attributes"):
            self.atom_attributes = pd.DataFrame(index=range(n_atoms))
        if len(self.atom_attributes.index) != n_atoms:
            if self.atom_attributes.shape[1] == 0:
                self.atom_attributes = pd.DataFrame(index=range(n_atoms))
            else:
                raise StructuralInconsistencyError(
                    reason=(
                        "Chemical-state atom attributes are not aligned with the stable atom inventory: "
                        f"{len(self.atom_attributes.index)} rows for {n_atoms} atoms."
                    ),
                    caller="molsysmt.native.topology._ChemicalStateStorage",
                )
        if not hasattr(self, "component_indices"):
            self.component_indices = pd.Series(
                pd.array([pd.NA] * n_atoms, dtype="Int64"), index=range(n_atoms)
            )
        elif len(self.component_indices.index) != n_atoms:
            if self.component_indices.isna().all():
                self.component_indices = pd.Series(
                    pd.array([pd.NA] * n_atoms, dtype="Int64"), index=range(n_atoms)
                )
            else:
                raise StructuralInconsistencyError(
                    reason=(
                        "Chemical-state component membership is not aligned with the stable atom inventory: "
                        f"{len(self.component_indices.index)} rows for {n_atoms} atoms."
                    ),
                    caller="molsysmt.native.topology._ChemicalStateStorage",
                )
        else:
            self.component_indices = pd.Series(
                pd.array(self.component_indices, dtype="Int64"), index=range(n_atoms)
            )
        if not hasattr(self, "_connectivity_completeness"):
            self._connectivity_completeness = "unavailable"
        if not hasattr(self, "_component_completeness"):
            self._component_completeness = "unavailable"
        if not hasattr(self, "_component_evidence"):
            self._component_evidence = "unknown"
        if not hasattr(self, "_provenance_index"):
            self._provenance_index = None
        if not hasattr(self, "_preparation_history"):
            self._preparation_history = []

        self._normalize_atom_attribute_columns()

    def _validate_atom_domain(self, n_atoms, *, check_component_indices=True):
        """Check current storage alignment without repairing or changing it.

        Legacy normalization belongs to explicit decoding. Native restrictions
        must not silently resize an unknown vector or mutate a source record.
        """
        expected = pd.RangeIndex(n_atoms)
        if (
            not isinstance(self.atom_attributes, pd.DataFrame)
            or not self.atom_attributes.index.equals(expected)
            or not isinstance(self.component_indices, pd.Series)
            or not self.component_indices.index.equals(expected)
            or str(self.component_indices.dtype) != "Int64"
        ):
            raise StructuralInconsistencyError(
                reason="Chemical-state atom rows must align with their stored atom domain.",
                caller="molsysmt.native.ChemicalStates",
            )
        if not isinstance(
            self.components, pd.DataFrame
        ) or not self.components.index.equals(pd.RangeIndex(len(self.components))):
            raise StructuralInconsistencyError(
                reason="Chemical-state component rows must use contiguous positional indices.",
                caller="molsysmt.native.ChemicalStates",
            )
        membership = self.component_indices.to_numpy(dtype=np.int64, na_value=-1)
        if check_component_indices and (
            self.component_indices.lt(0).any()
            or np.any(membership >= len(self.components))
        ):
            raise StructuralInconsistencyError(
                reason="Chemical-state component membership is outside its component inventory.",
                caller="molsysmt.native.ChemicalStates",
            )
        self._validated_atom_attributes(self.atom_attributes)

    def _normalize_atom_attribute_columns(self):
        """Validate names, order, and nullable dtypes of atom-state columns."""

        self.atom_attributes = self._validated_atom_attributes(self.atom_attributes)

    @classmethod
    def _validated_atom_attributes(cls, table):
        """Prepare a canonical table without publishing changes to a state."""

        unknown_columns = set(table.columns) - set(
            _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES
        )
        if unknown_columns:
            raise StructuralInconsistencyError(
                reason=f"Unknown chemical-state atom attributes: {sorted(unknown_columns)}.",
                caller="molsysmt.native.topology._ChemicalStateStorage",
            )
        ordered_columns = [
            name
            for name in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES
            if name in table.columns
        ]
        candidate = table.reindex(columns=ordered_columns)
        for name in ordered_columns:
            candidate[name] = cls._coerce_atom_attribute(name, candidate[name])
        return candidate

    @staticmethod
    def _coerce_atom_attribute(name, values):
        """Return one validated nullable array for an atom-state attribute."""

        if name not in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES:
            raise StructuralInconsistencyError(
                reason=f"Unknown chemical-state atom attribute {name!r}.",
                caller="molsysmt.native.topology._ChemicalStateStorage",
            )

        values = list(values)
        non_missing = [value for value in values if not pd.isna(value)]

        if name == "stereochemistry":
            invalid = sorted(
                {str(value) for value in non_missing}
                - _CHEMICAL_STATE_ATOM_STEREOCHEMISTRY_VALUES
            )
            if invalid:
                raise StructuralInconsistencyError(
                    reason=(
                        f"Invalid atom stereochemistry values {invalid}; expected values from "
                        f"{sorted(_CHEMICAL_STATE_ATOM_STEREOCHEMISTRY_VALUES)}."
                    ),
                    caller="molsysmt.native.topology._ChemicalStateStorage",
                )

        if _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name] == "boolean":
            invalid = [
                value
                for value in non_missing
                if not isinstance(value, (bool, np.bool_))
            ]
            if invalid:
                raise StructuralInconsistencyError(
                    reason=f"Chemical-state atom attribute {name!r} accepts only boolean or missing values.",
                    caller="molsysmt.native.topology._ChemicalStateStorage",
                )

        if _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name] in {"Int16", "UInt8"} and any(
            isinstance(value, (bool, np.bool_)) for value in non_missing
        ):
            raise StructuralInconsistencyError(
                reason=f"Chemical-state atom attribute {name!r} requires integer counts, not booleans.",
                caller="molsysmt.native.ChemicalStates",
            )

        try:
            return pd.array(values, dtype=_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name])
        except (TypeError, ValueError, OverflowError) as error:
            raise StructuralInconsistencyError(
                reason=(
                    f"Values for chemical-state atom attribute {name!r} cannot be represented as "
                    f"{_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name]}: {error}"
                ),
                caller="molsysmt.native.topology._ChemicalStateStorage",
            ) from error

    def _normalize_atom_indices(self, atom_indices):
        """Return validated atom indices for a partial atom-state operation."""

        indices = np.asarray(atom_indices)
        if indices.ndim != 1 or not np.issubdtype(indices.dtype, np.integer):
            raise StructuralInconsistencyError(
                reason="Chemical-state atom indices must be a one-dimensional integer sequence.",
                caller="molsysmt.native.topology._ChemicalStateStorage",
            )
        indices = indices.astype(np.int64, copy=False)
        if len(np.unique(indices)) != len(indices):
            raise StructuralInconsistencyError(
                reason="Chemical-state atom indices must not contain duplicates.",
                caller="molsysmt.native.topology._ChemicalStateStorage",
            )
        if np.any(indices < 0) or np.any(indices >= len(self.atom_attributes.index)):
            raise StructuralInconsistencyError(
                reason=(
                    f"Chemical-state atom indices are outside the valid range "
                    f"[0, {len(self.atom_attributes.index)})."
                ),
                caller="molsysmt.native.topology._ChemicalStateStorage",
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
                    f"Chemical-state atom attribute {name!r} received {len(values)} values; "
                    f"expected {expected_length}."
                ),
                caller="molsysmt.native.topology._ChemicalStateStorage",
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
                reason=f"Unknown chemical-state atom attribute {name!r}.",
                caller="molsysmt.native.topology._ChemicalStateStorage",
            )
        if name not in self.atom_attributes.columns:
            return None
        if atom_indices is None:
            return self.atom_attributes[name]
        indices = self._normalize_atom_indices(atom_indices)
        return self.atom_attributes[name].iloc[indices]

    def set_atom_attribute(self, name, values, atom_indices=None):
        """Set a complete or partial optional atom-state column."""

        self.atom_attributes = self._prepare_atom_attribute(name, values, atom_indices)

    def _prepare_atom_attribute(self, name, values, atom_indices=None):
        """Validate an atom-column replacement without changing the current table."""

        if name not in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES:
            raise StructuralInconsistencyError(
                reason=f"Unknown chemical-state atom attribute {name!r}.",
                caller="molsysmt.native.topology._ChemicalStateStorage",
            )
        if atom_indices is None:
            normalized_values = self._values_with_length(
                values, len(self.atom_attributes.index), name
            )
            column = self._coerce_atom_attribute(name, normalized_values)
        else:
            indices = self._normalize_atom_indices(atom_indices)
            normalized_values = self._values_with_length(values, len(indices), name)
            if name not in self.atom_attributes.columns:
                column = pd.array(
                    [pd.NA] * len(self.atom_attributes.index),
                    dtype=_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES[name],
                )
            else:
                column = self.atom_attributes[name].array.copy()
            coerced_values = self._coerce_atom_attribute(name, normalized_values)
            column[indices] = coerced_values
        candidate = self.atom_attributes.copy(deep=False)
        candidate[name] = column
        return self._validated_atom_attributes(candidate)

    def remove_atom_attribute(self, name):
        """Remove an optional atom-state column if it is materialized."""

        if name not in _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES:
            raise StructuralInconsistencyError(
                reason=f"Unknown chemical-state atom attribute {name!r}.",
                caller="molsysmt.native.topology._ChemicalStateStorage",
            )
        if name in self.atom_attributes.columns:
            del self.atom_attributes[name]

    def copy(self):
        """Copying current private state without construction or normalization."""
        from copy import deepcopy

        return deepcopy(self)


def _coerce_bond_table(value, n_atoms=None):
    """Normalize canonical or legacy bond storage into the v1 schema."""

    if not isinstance(value, pd.DataFrame):
        raise StructuralInconsistencyError(
            reason="Chemical-state bonds must be provided as a Pandas DataFrame.",
            caller="molsysmt.native.Topology",
        )

    required_columns = {"atom1_index", "atom2_index"}
    missing_columns = required_columns - set(value.columns)
    if missing_columns:
        raise StructuralInconsistencyError(
            reason=f"Chemical-state bond table is missing required columns: {sorted(missing_columns)}.",
            caller="molsysmt.native.Topology",
        )

    unexpected_columns = set(value.columns) - _BOND_ALLOWED_COLUMNS - {"order", "type"}
    if unexpected_columns:
        raise StructuralInconsistencyError(
            reason=f"Chemical-state bond table has unsupported columns: {sorted(unexpected_columns)}.",
            caller="molsysmt.native.Topology",
        )

    output = Bonds_DataFrame(n_bonds=value.shape[0])
    try:
        output["atom1_index"] = pd.array(value["atom1_index"], dtype="Int64")
        output["atom2_index"] = pd.array(value["atom2_index"], dtype="Int64")
    except (TypeError, ValueError, OverflowError) as error:
        raise StructuralInconsistencyError(
            reason=f"Bond endpoint indices must be integers: {error}",
            caller="molsysmt.native.Topology",
        ) from error

    if output[list(_BOND_REQUIRED_COLUMNS)].isna().any(axis=None):
        raise StructuralInconsistencyError(
            reason="Bond endpoint indices must not be missing.",
            caller="molsysmt.native.Topology",
        )

    atom1 = output["atom1_index"].to_numpy(dtype=np.int64)
    atom2 = output["atom2_index"].to_numpy(dtype=np.int64)
    if np.any(atom1 == atom2):
        raise StructuralInconsistencyError(
            reason="Self-bonds are not valid chemical-state edges.",
            caller="molsysmt.native.Topology",
        )
    if n_atoms is not None and (
        np.any(atom1 < 0)
        or np.any(atom2 < 0)
        or np.any(atom1 >= n_atoms)
        or np.any(atom2 >= n_atoms)
    ):
        raise StructuralInconsistencyError(
            reason=f"Bond endpoint indices must be between 0 and {n_atoms - 1}.",
            caller="molsysmt.native.Topology",
        )

    swap = atom1 > atom2
    if np.any(swap):
        atom1[swap], atom2[swap] = atom2[swap].copy(), atom1[swap].copy()
        output["atom1_index"] = pd.array(atom1, dtype="Int64")
        output["atom2_index"] = pd.array(atom2, dtype="Int64")
    if len(set(zip(atom1.tolist(), atom2.tolist()))) != len(atom1):
        raise StructuralInconsistencyError(
            reason="Only one bond is allowed per unordered atom pair.",
            caller="molsysmt.native.Topology",
        )

    for column, dtype in _BOND_OPTIONAL_DTYPES.items():
        if column in value.columns:
            try:
                output[column] = pd.array(value[column], dtype=dtype)
            except (TypeError, ValueError, OverflowError) as error:
                raise StructuralInconsistencyError(
                    reason=f"Invalid values for bond field {column!r}: {error}",
                    caller="molsysmt.native.Topology",
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
                    f"Conflicting legacy and canonical bond values for {column!r} "
                    f"at row {row_index}."
                ),
                caller="molsysmt.native.Topology",
            )
        try:
            output.at[row_index, column] = normalized_value
        except (TypeError, ValueError, OverflowError) as error:
            raise StructuralInconsistencyError(
                reason=(
                    f"Legacy bond value {normalized_value!r} cannot be represented "
                    f"in canonical field {column!r}: {error}"
                ),
                caller="molsysmt.native.Topology",
            ) from error

    order_aliases = {"single": 1, "double": 2, "triple": 3, "quadruple": 4}

    def _normalize_legacy_label(raw_value, field, row_index):
        if _missing(raw_value):
            return
        if isinstance(raw_value, (bool, np.bool_)):
            raise StructuralInconsistencyError(
                reason=f"Boolean values are not valid legacy bond {field}.",
                caller="molsysmt.native.Topology",
            )
        if isinstance(raw_value, (int, float, np.integer, np.floating)):
            numeric_value = float(raw_value)
            if not np.isfinite(numeric_value) or numeric_value < 0:
                raise StructuralInconsistencyError(
                    reason=f"Invalid legacy bond {field} value {raw_value!r}.",
                    caller="molsysmt.native.Topology",
                )
            if numeric_value.is_integer():
                _set_value(row_index, "bond_order", int(numeric_value))
            else:
                _set_value(row_index, "fractional_bond_order", numeric_value)
            return

        label = str(raw_value).strip().lower()
        if label in {"", "none", "<na>", "nan", "unspecified"}:
            return
        if label in order_aliases:
            _set_value(row_index, "bond_order", order_aliases[label])
            return
        if label == "aromatic":
            _set_value(row_index, "is_aromatic", True)
            return
        if label in {"covalent", "dative", "unknown"}:
            _set_value(row_index, "bond_type", label)
            return
        try:
            numeric_value = float(label)
        except ValueError as error:
            raise StructuralInconsistencyError(
                reason=(
                    f"Legacy bond {field} value {raw_value!r} has no unambiguous "
                    "mapping to the normalized chemical schema."
                ),
                caller="molsysmt.native.Topology",
            ) from error
        _normalize_legacy_label(numeric_value, field, row_index)

    for legacy_column in ("order", "type"):
        if legacy_column in value.columns:
            for row_index, raw_value in enumerate(value[legacy_column].tolist()):
                _normalize_legacy_label(raw_value, legacy_column, row_index)

    if "bond_type" in output.columns:
        allowed_bond_types = {"covalent", "dative", "unknown"}
        invalid = set(output["bond_type"].dropna().tolist()) - allowed_bond_types
        if invalid:
            raise StructuralInconsistencyError(
                reason=f"Invalid canonical bond_type values: {sorted(invalid)}.",
                caller="molsysmt.native.Topology",
            )
        if "joins_components" not in output.columns:
            output["joins_components"] = pd.array(
                [pd.NA] * len(output.index), dtype="boolean"
            )
        covalent = output["bond_type"].eq("covalent").fillna(False)
        dative = output["bond_type"].eq("dative").fillna(False)
        explicit_override = (
            covalent & output["joins_components"].eq(False).fillna(False)
        ) | (dative & output["joins_components"].eq(True).fillna(False))
        if explicit_override.any():
            if (
                "evidence" not in output.columns
                or output.loc[explicit_override, "evidence"].isna().any()
            ):
                raise StructuralInconsistencyError(
                    reason=(
                        "A non-default joins_components value requires explicit "
                        "bond evidence."
                    ),
                    caller="molsysmt.native.Topology",
                )
        output.loc[covalent & output["joins_components"].isna(), "joins_components"] = (
            True
        )
        output.loc[dative & output["joins_components"].isna(), "joins_components"] = (
            False
        )

    if "joins_components" in output.columns:
        lacks_default = output["joins_components"].notna()
        if "bond_type" in output.columns:
            lacks_default &= ~output["bond_type"].isin(["covalent", "dative"])
        if lacks_default.any() and (
            "evidence" not in output.columns
            or output.loc[lacks_default, "evidence"].isna().any()
        ):
            raise StructuralInconsistencyError(
                reason=(
                    "joins_components without a covalent or dative default "
                    "requires explicit bond evidence."
                ),
                caller="molsysmt.native.Topology",
            )

    if "evidence" in output.columns:
        invalid = (
            set(output["evidence"].dropna().tolist()) - _CHEMICAL_STATE_EVIDENCE_VALUES
        )
        if invalid:
            raise StructuralInconsistencyError(
                reason=f"Invalid bond evidence values: {sorted(invalid)}.",
                caller="molsysmt.native.Topology",
            )

    if "fractional_bond_order" in output.columns:
        fractional_orders = (
            output["fractional_bond_order"].dropna().to_numpy(dtype=float)
        )
        if np.any(~np.isfinite(fractional_orders)) or np.any(fractional_orders < 0):
            raise StructuralInconsistencyError(
                reason="Fractional bond order must be finite and non-negative.",
                caller="molsysmt.native.Topology",
            )
    if "provenance_index" in output.columns:
        provenance_indices = (
            output["provenance_index"].dropna().to_numpy(dtype=np.int64)
        )
        if np.any(provenance_indices < 0):
            raise StructuralInconsistencyError(
                reason="Bond provenance indices must be non-negative.",
                caller="molsysmt.native.Topology",
            )

    for column in (
        "stereo_atom1_index",
        "stereo_atom2_index",
        "donor_atom_index",
        "acceptor_atom_index",
    ):
        if column in output.columns and n_atoms is not None:
            indices = output[column].dropna().to_numpy(dtype=np.int64)
            if np.any(indices < 0) or np.any(indices >= n_atoms):
                raise StructuralInconsistencyError(
                    reason=f"Bond field {column!r} contains atom indices outside the topology.",
                    caller="molsysmt.native.Topology",
                )

    for column in ("donor_atom_index", "acceptor_atom_index"):
        if column in output.columns:
            invalid_reference = output[column].notna() & ~(
                output[column].eq(output["atom1_index"])
                | output[column].eq(output["atom2_index"])
            )
            if invalid_reference.any():
                raise StructuralInconsistencyError(
                    reason=f"Bond field {column!r} must reference one of the bond endpoints.",
                    caller="molsysmt.native.Topology",
                )
    if {"donor_atom_index", "acceptor_atom_index"} <= set(output.columns):
        same_directional_endpoint = (
            output["donor_atom_index"].notna()
            & output["acceptor_atom_index"].notna()
            & output["donor_atom_index"].eq(output["acceptor_atom_index"])
        )
        if same_directional_endpoint.any():
            raise StructuralInconsistencyError(
                reason="Bond donor and acceptor atom indices must be distinct.",
                caller="molsysmt.native.Topology",
            )

    if "stereochemistry" in output.columns:
        has_stereochemistry = output["stereochemistry"].notna()
        missing_references = pd.Series(False, index=output.index)
        for column in ("stereo_atom1_index", "stereo_atom2_index"):
            if column not in output.columns:
                missing_references |= has_stereochemistry
            else:
                missing_references |= has_stereochemistry & output[column].isna()
        if missing_references.any():
            raise StructuralInconsistencyError(
                reason="Bond stereochemistry requires two stereo reference atom indices.",
                caller="molsysmt.native.Topology",
            )

    output._fix_null_values()
    output._remove_empty_columns()
    output._sort_bonds()
    return output


def _concatenate_bond_tables(*tables, n_atoms=None):
    """Concatenate bond storage without all-missing optional dtype drift."""
    required_columns = {"atom1_index", "atom2_index"}
    prepared = []
    for table in tables:
        keep_columns = [
            column
            for column in table.columns
            if column in required_columns or table[column].notna().any()
        ]
        prepared.append(table.loc[:, keep_columns])
    return _coerce_bond_table(pd.concat(prepared, ignore_index=True), n_atoms=n_atoms)


def _remap_bond_atom_indices(table, index_map, *, canonical_order=False):
    """Remap atom references, optionally orienting endpoints and stereo neighbors."""

    output = table.copy()
    for column in _BOND_ATOM_REFERENCE_COLUMNS:
        if column in output.columns:
            original = output[column]
            remapped = original.map(index_map)
            if column in {"atom1_index", "atom2_index"} and remapped.isna().any():
                raise StructuralInconsistencyError(
                    reason="Bond endpoints cannot be retained when their atoms are absent.",
                    caller="molsysmt.native.Topology",
                )
            output[column] = pd.array(remapped, dtype="Int64")

    if canonical_order:
        swapped = output["atom1_index"] > output["atom2_index"]
        for first, second in (
            ("atom1_index", "atom2_index"),
            ("stereo_atom1_index", "stereo_atom2_index"),
        ):
            if first in output and second in output:
                saved = output.loc[swapped, first].copy()
                output.loc[swapped, first] = output.loc[swapped, second]
                output.loc[swapped, second] = saved
    stereo_columns = {"stereo_atom1_index", "stereo_atom2_index"} & set(output.columns)
    if stereo_columns:
        incomplete_stereo = output[list(stereo_columns)].isna().any(axis=1)
        for column in (
            "stereo_atom1_index",
            "stereo_atom2_index",
            "stereochemistry",
        ):
            if column in output.columns:
                output.loc[incomplete_stereo, column] = pd.NA
    return output
