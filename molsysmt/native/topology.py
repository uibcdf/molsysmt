from contextlib import nullcontext

import numpy as np
import pandas as pd
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.variables import is_all

from . import _chemical_state as _chemical_storage
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
    """Holding only a stable atom inventory and represented hierarchy.

    Subclasses inheriting the constructor retain its native count validation,
    including when the subclass is defined in another module. Ordinary user
    construction does not require skip_digestion.
    """

    def __repr__(self):
        """Summarizing stored metadata without reading or rendering payloads."""
        from ._repr import summary, topology_fields

        return summary(self, **topology_fields(self))

    def __setattr__(self, name, value):
        if name in {
            "chemical_states",
            "bonds",
            "components",
            "_chemical_states_domain",
        }:
            raise AttributeError(
                "Topology has no chemical_states attribute; assign chemical states through MolSys.chemical_states."
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
        """Copying stable inventory tables without chemical storage."""
        from ._copy import _clone

        result = _clone(self, memo, exclude=("_molsys_owner_ref",))
        # Pandas' default constructor erases our canonical table subclasses.
        # Retype the independent copied table in place, preserving memo aliases.
        for name in ("atoms", "groups", "molecules", "entities", "chains"):
            source = getattr(self, name)
            if type(source) in (
                Atoms_DataFrame,
                Groups_DataFrame,
                Molecules_DataFrame,
                Entities_DataFrame,
                Chains_DataFrame,
            ):
                getattr(result, name).__class__ = type(source)
        return result

    @arg_digest(native_constructor="molsysmt.native.topology.__init__")
    def __init__(
        self,
        n_atoms=0,
        n_groups=0,
        n_molecules=0,
        n_entities=0,
        n_chains=0,
        skip_digestion=False,
    ):
        """Initialize only stable inventory and represented hierarchy tables."""
        self._chain_group_membership = None
        self._atom_molecule_membership = None
        self.reset_atoms(n_atoms=n_atoms)
        self.reset_groups(n_groups=n_groups)
        self.reset_molecules(n_molecules=n_molecules)
        self.reset_entities(n_entities=n_entities)
        self.reset_chains(n_chains=n_chains)
        self._coerce_id_columns_to_string()
        self._atoms_dirty = self._groups_dirty = self._molecules_dirty = False
        self._entities_dirty = self._chains_dirty = False

    def __setstate__(self, state):
        """Restore a pure inventory snapshot; reject legacy chemical ownership."""
        if any(
            name in state
            for name in (
                "bonds",
                "components",
                "_chemical_states",
                "_reference_chemical_state",
                "_chemical_states_domain",
                "atoms_dataframe",
            )
        ):
            raise ValueError(
                "Legacy Topology pickle carries chemistry and cannot be restored as pure Topology. Load it with the MolSysMT version that wrote it, export the complete molecular system to H5MSM, then read or migrate that file with this version."
            )
        state = dict(state)
        state.pop("_molsys_owner_ref", None)
        self.__dict__.update(state)
        self.__dict__.setdefault("_atom_molecule_membership", None)
        self.__dict__.setdefault("_chain_group_membership", None)
        if "isotope" not in self.atoms:
            self.atoms.insert(
                3, "isotope", pd.array([pd.NA] * self.n_atoms, dtype="UInt16")
            )

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

    def get_n_molecules(self):
        return self.molecules.shape[0]

    def get_n_entities(self):
        return self.entities.shape[0]

    def get_n_chains(self):
        return self.chains.shape[0]

    def reset_atoms(self, n_atoms=0):
        """Reset stable atom rows without silently resizing an attached molecular axis."""
        n_atoms = int(n_atoms)
        current = len(getattr(self, "atoms", ()))
        if n_atoms != current:
            owner_ref = getattr(self, "_molsys_owner_ref", None)
            if owner_ref is not None and owner_ref() is not None:
                raise StructuralInconsistencyError(
                    reason="An attached atom axis must be resized through its owning MolSys."
                )
            if getattr(self, "_atom_molecule_membership", None) is not None:
                raise StructuralInconsistencyError(
                    reason="Resetting atom count would discard declared molecule membership; use extraction or coordinated editing."
                )
        self.atoms = Atoms_DataFrame(n_atoms=n_atoms)
        self._atom_molecule_membership = None

    def reset_groups(self, n_groups=0):
        """Reset groups table to a new size."""

        self.groups = Groups_DataFrame(n_groups=n_groups)
        self._chain_group_membership = None

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

    def _coerce_id_columns_to_string(self):
        """Ensure all *_id columns use pandas string dtype."""

        self.atoms["atom_id"] = self.atoms["atom_id"].astype("string")
        self.groups["group_id"] = self.groups["group_id"].astype("string")
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
    def n_molecules(self):
        return self.molecules.shape[0]

    @property
    def n_entities(self):
        return self.entities.shape[0]

    @property
    def n_chains(self):
        return self.chains.shape[0]

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
        """Append stable inventory and hierarchy without reading chemical records."""
        from ._atom_molecules import compact, stored
        from ._chain_groups import by_chain

        owner_ref = getattr(self, "_molsys_owner_ref", None)
        if owner_ref is not None and owner_ref() is not None:
            raise StructuralInconsistencyError(
                reason="An attached atom axis must grow through its owning MolSys."
            )
        other = (
            item.copy()
            if is_all(atom_indices)
            else item.extract(
                atom_indices=atom_indices, copy_if_all=True, skip_digestion=True
            )
        )
        atoms, groups, molecules, entities, chains = (
            self.n_atoms,
            self.n_groups,
            self.n_molecules,
            self.n_entities,
            self.n_chains,
        )
        declared = (
            self._chain_group_membership is not None
            or other._chain_group_membership is not None
        )
        chain_groups = (
            (
                [values.tolist() for values in by_chain(self)]
                + [(values + groups).tolist() for values in by_chain(other)]
            )
            if declared
            else None
        )
        left, right = stored(self), stored(other)
        membership = None
        if left is not None or right is not None:
            left = np.full(atoms, -1, dtype=np.int64) if left is None else left
            right = (
                np.full(other.n_atoms, -1, dtype=np.int64)
                if right is None
                else right.copy()
            )
            right[right >= 0] += molecules
            membership = compact(np.concatenate([left, right]))
        other.atoms["group_index"] += groups
        other.atoms["chain_index"] += chains
        other.groups["molecule_index"] += molecules
        other.molecules["entity_index"] += entities
        for name in ("atoms", "groups", "molecules", "entities", "chains"):
            setattr(
                self,
                name,
                pd.concat(
                    [getattr(self, name), getattr(other, name)], ignore_index=True
                ),
            )
        self._atom_molecule_membership = membership
        if declared:
            self.set_chain_groups(chain_groups)
        # The concatenated declarations are authoritative. Re-inference here
        # would replace group-free molecule labels and merge distinct entities.
        if not keep_ids:
            from ._topology_infer import fallback_ids, infer_chain_ids_from_topology

            for name, singular in (
                ("atoms", "atom"),
                ("groups", "group"),
                ("molecules", "molecule"),
                ("entities", "entity"),
            ):
                getattr(self, name)[singular + "_id"] = fallback_ids(
                    len(getattr(self, name))
                )
            self.chains["chain_id"] = infer_chain_ids_from_topology(self)
        self._coerce_id_columns_to_string()

    @signal(tags=["native"])
    @arg_digest()
    def copy(self, *, skip_digestion=False):
        """Copying canonical stable inventory and memberships independently.

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
        Membership is inferred only from stable group/chain inventory when
        requested. Explicit group-free atom-to-molecule membership is retained;
        this method neither reads components nor chooses a chemical state.
        Atom-free groups and empty declared molecule slots remain representable.
        Establish component-derived membership explicitly during construction,
        rather than refreshing it after chemical connectivity edits. This native
        operation is not form-agnostic.
        """
        from ._topology_infer import (
            complete_missing_molecule_membership,
            fallback_ids,
            infer_molecule_indices_from_topology,
            infer_molecule_names_from_topology,
            infer_molecule_types_from_topology,
        )

        if self.n_atoms == 0:
            complete_missing_molecule_membership(self)
        elif self.n_groups and (
            redefine_indices or force or self.groups["molecule_index"].isna().any()
        ):
            values = infer_molecule_indices_from_topology(self)
            self.groups["molecule_index"] = pd.array(values, dtype="Int64")
            self.reset_molecules(
                n_molecules=int(np.max(values)) + 1 if len(values) else 0
            )
        if redefine_ids:
            self.molecules["molecule_id"] = fallback_ids(self.n_molecules)
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
        self.molecules._fix_null_values()
        self.entities._fix_null_values()
        self.chains._fix_null_values()
        self._coerce_id_columns_to_string()

    @arg_digest()
    def compare(
        self, item, rule="equal", output_type="boolean", skip_digestion=False, **kwargs
    ):
        """Compare stable topology content with another topology."""
        self._reject_chemical_filters(kwargs)

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

        if output_type == "boolean":
            output = all(list(output.values()))

        return output

    @staticmethod
    def _reject_chemical_filters(values):
        from molsysmt._private.smonitor import ArgumentError
        from molsysmt.attribute.attributes import attributes

        for name, value in values.items():
            if (
                "bond" in name
                or "component" in name
                or attributes.get(name, {}).get("chemical_state", False)
            ):
                if value is not False and value is not None:
                    raise ArgumentError(
                        name,
                        value=value,
                        caller="molsysmt.Topology",
                        message="Chemical queries require ChemicalStates or an owning MolSys.",
                    )

    def get_atom_indices(self, **kwargs):
        """Select atom indices matching the provided hierarchical filters."""
        self._reject_chemical_filters(kwargs)

        for aux in kwargs:
            if isinstance(kwargs[aux], (str, int)):
                kwargs[aux] = [kwargs[aux]]
            if aux.endswith("_id") and kwargs[aux] is not None:
                kwargs[aux] = [str(ii) for ii in kwargs[aux]]

        atom_columns = []
        group_columns = []
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

        if len(chain_columns):
            if "chain_index" not in atom_columns:
                atom_columns.append("chain_index")

        from molsysmt._private.topology_expansion import expand_atom_dataframe

        aux_df = expand_atom_dataframe(
            self,
            atom_columns=atom_columns,
            group_columns=group_columns,
            component_columns=(),
            molecule_columns=molecule_columns,
            entity_columns=entity_columns,
            chain_columns=chain_columns,
        )

        mask = pd.Series(True, index=aux_df.index)

        for col, valores in kwargs.items():
            mask &= aux_df[col].isin(valores)

        return aux_df.index[mask].tolist()
