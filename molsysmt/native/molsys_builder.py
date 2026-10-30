from __future__ import annotations

import numpy as np
import pandas as pd
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, StructuralInconsistencyError

from .queries import NativeQueries


class MolSysBuilder(NativeQueries):
    """Building a native molecular system incrementally from declared elements.

    Notes
    -----
    A builder stores editable chemical/topological and structural native
    components. Their complete declared attribute union is available through
    :func:`molsysmt.get` without first calling :meth:`build`. Molecular
    mechanics and named interaction analyses are not stored by
    this object.
    """

    def __repr__(self):
        """Summarizing stored metadata without reading or rendering payloads."""
        from ._repr import size, structure_dimensions, summary

        n_structures, _ = structure_dimensions(vars(self).get("structures"))
        topology = vars(self).get("topology")
        data = {} if topology is None else vars(topology)
        return summary(
            self,
            n_atoms=size(data.get("atoms")),
            n_groups=size(data.get("groups")),
            n_structures=n_structures,
        )

    @signal(tags=["native", "builder"])
    def __init__(self, molecular_system=None, skip_digestion=False):

        from .molsys import MolSys
        from .structures import Structures

        if molecular_system is None:
            initial = MolSys(skip_digestion=True)
            self.topology = initial.topology.copy()
            self.chemical_states = initial.chemical_states.copy()
            self.structures = Structures(skip_digestion=True)
            self._structure_chemical_state_indices = None
            self._dirty_chemical_states = {0}
        elif isinstance(molecular_system, MolSys):
            self.topology = molecular_system.topology.copy()
            self.structures = molecular_system.structures.copy()
            self.chemical_states = (
                None
                if molecular_system.chemical_states is None
                else molecular_system.chemical_states.copy()
            )
            association = molecular_system._structure_chemical_state_indices
            self._structure_chemical_state_indices = (
                None if association is None else association.copy()
            )
            self._dirty_chemical_states = set()
            self._preserve_absent_groups = (
                self.topology.n_groups == 0 and self.topology.n_molecules > 0
            )
            self._capture_group_free_molecule_membership()
        else:
            raise ArgumentChoiceError(
                argument="molecular_system",
                value=molecular_system,
                choices=["None", "molsysmt.MolSys"],
                caller="molsysmt.native.MolSysBuilder.__init__",
                message="MolSysBuilder can only be initialized from None or molsysmt.MolSys.",
            )

    @property
    def n_atoms(self):
        return self.topology.n_atoms

    @property
    def n_groups(self):
        return self.topology.n_groups

    @property
    def n_bonds(self):
        return len(self._chemical_state().bonds)

    @property
    def n_chains(self):
        return self.topology.n_chains

    @property
    def n_molecules(self):
        return self.topology.n_molecules

    @property
    def n_entities(self):
        return self.topology.n_entities

    @property
    def n_structures(self):
        return self.structures.n_structures

    @arg_digest()
    def copy(self, deep=True, *, skip_digestion=False):
        """Copying an editable staging system without compiling it.

        Parameters
        ----------
        deep : bool, default=True
            Copy coordinate/box bytes eagerly. False shares protected geometry
            until edits replace affected blocks. Canonical staging tables,
            other mutable series and metadata remain independent in both modes.
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        MolSysBuilder
            An independent builder preserving its concrete type and declared data.

        Notes
        -----
        Python copy.copy uses deferred geometry allocation; copy.deepcopy uses
        eager geometry allocation and the enclosing graph's memo. Copying does
        not call build(), synthesize parents, normalize tables or invent domains.
        A partially assembled builder remains partially assembled. The builder
        stores no named analyses or mechanics; explicit structure/state associations are retained.

        Examples
        --------
        >>> builder = MolSysBuilder()
        >>> builder.add_atom(atom_name='C', atom_type='C')
        0
        >>> duplicate = builder.copy(deep=False)
        >>> duplicate.n_atoms, duplicate.n_groups
        (1, 0)

        .. admonition:: User guide

           See :ref:`user-foundations-resident-copying` and :ref:`Tutorial_Editable`.

        .. versionadded:: 1.0.0
        """
        from ._copy import _copy_independently

        if deep:
            return _copy_independently(self, skip_digestion)
        if not isinstance(skip_digestion, bool):
            from molsysmt._private.argdigest.argument.skip_digestion import (
                digest_skip_digestion,
            )

            digest_skip_digestion(skip_digestion)
        return self.__copy__()

    def __copy__(self):
        """Copying independent staging state over protected geometry blocks."""
        from ._copy import _clone, _deferred_geometry_memo

        return _clone(self, _deferred_geometry_memo(self.structures))

    def __deepcopy__(self, memo):
        """Copying current staging data with the containing graph's memo."""
        from ._copy import _clone

        return _clone(self, memo)

    def _ensure_atom_editable(self):
        if (
            self.structures.coordinates is not None
            or self.structures.velocities is not None
            or self.structures.b_factor is not None
        ):
            raise StructuralInconsistencyError(
                caller="molsysmt.native.MolSysBuilder",
                reason="Atoms cannot be added after atom-dependent structural arrays have been assigned.",
            )

    @staticmethod
    def _normalize_optional_string(value, default=None):
        if value is None:
            return default
        return str(value)

    @staticmethod
    def _normalize_optional_float(value):
        if value is None:
            return pd.NA
        return value

    @staticmethod
    def _indices_array(indices):
        from molsysmt._private.smonitor import StructuralInconsistencyError

        values = np.asarray(indices, dtype=int)
        if values.ndim != 1:
            raise StructuralInconsistencyError(
                "Indices must define a one-dimensional collection."
            )
        return values

    def _validate_existing_indices(self, indices, *, upper_bound, element_name):
        from molsysmt._private.smonitor import StructuralInconsistencyError

        if len(indices) == 0:
            raise StructuralInconsistencyError(
                f"{element_name} membership cannot be empty."
            )
        if np.any(indices < 0) or np.any(indices >= upper_bound):
            raise StructuralInconsistencyError(
                f"{element_name} membership references undefined lower-level indices."
            )

    @staticmethod
    def _fill_missing_string_ids(values):
        output = values.astype("string").copy()
        for index in range(len(output)):
            if pd.isna(output.iloc[index]):
                output.iloc[index] = str(index)
        return output

    @signal(tags=["native", "builder"])
    @arg_digest()
    def add_atom(
        self, atom_id=None, atom_name=None, atom_type=None, skip_digestion=False
    ):
        """Appending an atom and aligned unknown rows to every chemical state.

        Parameters
        ----------
        atom_id : str or int, optional
            Atom label, normalized to a string. None uses the new atom index.
        atom_name : str, optional
            Atom name. None uses UNK.
        atom_type : str, optional
            Element symbol in MolSysMT terminology. None uses the existing
            atom-name interpretation tool, with its unknown-name diagnostic.
        skip_digestion : bool, default=False
            Whether to skip argument digestion for already validated arguments.

        Returns
        -------
        int
            Appended atom index in the stable native inventory.

        Raises
        ------
        StructuralInconsistencyError
            If atom-dependent structure arrays are present or existing chemical
            records are misaligned or invalid. Validation precedes publication.

        Notes
        -----
        All chemical states retain their existing atom assignments, bonds,
        component tables, labels, reference selection and producer history.
        The new rows have missing chemical assignments and component membership,
        preserving nullable dtypes. Complete connectivity/component declarations
        become partial; unavailable declarations are not upgraded. No formal
        charge, valence, hydrogen count or aromaticity is guessed.

        Adding an atom is inventory editing, not chemical preparation. Scientific
        tools can reject the incomplete resulting state until it is explicitly
        completed and satisfies their method profile. Validation errors leave
        the builder inventory and all chemical-state tables unchanged. Existing
        coordinates, velocities or B factors forbid atom addition; no structural
        arrays are silently resized. The source used to initialize a builder
        remains independent. Publication is not a concurrent-edit transaction.

        Examples
        --------
        >>> builder = MolSysBuilder()
        >>> builder.add_atom(atom_id=7, atom_name='C', atom_type='C')
        0
        >>> builder.topology.atoms.atom_id.tolist()
        ['7']

        .. admonition:: User guide

           See :ref:`Tutorial_Editable` and :ref:`Cookbook_Group_Free_Hierarchy`.

        .. versionadded:: 1.0.0
        """

        from molsysmt.element.atom import get_atom_type_from_atom_name

        self._ensure_atom_editable()

        atom_index = self.topology.n_atoms
        if (
            self.chemical_states is not None
            and self.chemical_states.n_atoms != atom_index
        ):
            raise StructuralInconsistencyError(
                caller="molsysmt.native.MolSysBuilder.add_atom",
                reason="Existing topology and chemical-state atom domains must align.",
            )
        if not self.topology.atoms.index.equals(pd.RangeIndex(atom_index)):
            raise StructuralInconsistencyError(
                caller="molsysmt.native.MolSysBuilder.add_atom",
                reason="Existing atom rows must follow the stable atom-index domain.",
            )
        atom_name = self._normalize_optional_string(atom_name, default="UNK")
        if atom_type is None:
            atom_type = get_atom_type_from_atom_name(atom_name)
        self._capture_group_free_molecule_membership()
        # Normalize and stage stable inventory before growing any owned states.
        atoms = self.topology.atoms.copy(deep=True)
        atoms.loc[atom_index, "atom_id"] = self._normalize_optional_string(
            atom_id, default=str(atom_index)
        )
        atoms.loc[atom_index, "atom_name"] = atom_name
        atoms.loc[atom_index, "atom_type"] = self._normalize_optional_string(
            atom_type, default="UNK"
        )
        atoms.loc[atom_index, "group_index"] = pd.NA
        atoms.loc[atom_index, "chain_index"] = pd.NA
        atoms["atom_id"] = atoms["atom_id"].astype("string")
        atoms["group_index"] = atoms["group_index"].astype("Int64")
        atoms["chain_index"] = atoms["chain_index"].astype("Int64")
        if "isotope" in atoms:
            atoms["isotope"] = atoms["isotope"].astype("UInt16")
        from ._atom_molecules import compact, stored

        direct = stored(self.topology)
        membership = None if direct is None else compact(np.r_[direct, np.int64(-1)])
        if self.chemical_states is not None:
            self.chemical_states._extend_atom_domain(atom_index + 1)
            self._dirty_chemical_states.update(
                range(self.chemical_states.n_chemical_states)
            )
        self.topology.atoms = atoms
        self.topology._atom_molecule_membership = membership

        return atom_index

    def _capture_group_free_molecule_membership(self):
        """Retain source ownership during the transition to group-based membership."""
        if (
            not hasattr(self, "_inherited_atom_molecules")
            and self.topology.n_groups == 0
            and self.topology.n_molecules > 0
        ):
            from ._topology_infer import molecule_indices_from_atoms

            self._inherited_atom_molecules = molecule_indices_from_atoms(
                self.topology
            ).copy()

    def _inherited_group_molecule(self, atom_indices):
        """Resolve one inherited owner without merging declared source molecules."""
        from ._atom_molecules import resolve

        candidates = np.unique(resolve(self.topology)[atom_indices])
        candidates = candidates[candidates >= 0]
        if len(candidates) > 1:
            raise StructuralInconsistencyError(
                caller="molsysmt.native.MolSysBuilder.add_group",
                reason="A group cannot span multiple inherited source molecules.",
            )
        return int(candidates[0]) if len(candidates) else pd.NA

    @signal(tags=["native", "builder"])
    @arg_digest()
    def add_group(
        self,
        atom_indices,
        group_id=None,
        group_name=None,
        group_type=None,
        skip_digestion=False,
    ):
        """Adding a group while preserving inherited source molecule ownership.

        Parameters
        ----------
        atom_indices : list, tuple, or numpy.ndarray
            Existing atom indices to assign to this group. Atoms must be ungrouped.
            An empty collection declares a group without stored atoms.
        group_id : str or int, optional
            Group label, normalized to a string. None uses its new index.
        group_name : str, optional
            Group name. None uses UNK.
        group_type : str, optional
            Group type. None leaves it available for inference at build time.
        skip_digestion : bool, default=False
            Whether to skip argument digestion for already validated arguments.

        Returns
        -------
        int
            Index of the appended group.

        Raises
        ------
        StructuralInconsistencyError
            If atoms are undefined, already grouped, or span distinct inherited
            source molecules. A rejected group is not partially inserted.

        Notes
        -----
        When staging a group-free source, added groups inherit its molecule
        indices and metadata. Building fills remaining ungrouped source atoms
        with fallback groups retaining the same ownership. New builders without
        an inherited molecule axis retain their ordinary inference behavior.
        Membership staging uses a compact source-atom map; no new chemical store
        or implicit molecular merge is introduced.

        Examples
        --------
        >>> builder = MolSysBuilder()
        >>> atom_index = builder.add_atom(atom_name='C', atom_type='C')
        >>> builder.add_group([atom_index], group_name='LIG')
        0

        .. admonition:: User guide

           See :ref:`Tutorial_Editable` for staging and compiling native edits.

        .. versionadded:: 1.0.0
        """
        atom_indices = self._indices_array(atom_indices)
        if len(atom_indices):
            self._validate_existing_indices(
                atom_indices, upper_bound=self.topology.n_atoms, element_name="Group"
            )

        current_group_index = self.topology.atoms.loc[atom_indices, "group_index"]
        if current_group_index.notna().any():
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                "Atoms already assigned to a group cannot be reassigned."
            )

        self._capture_group_free_molecule_membership()
        molecule_index = self._inherited_group_molecule(atom_indices)
        from ._atom_molecules import compact, stored

        direct = stored(self.topology)
        membership = None
        if direct is not None:
            membership = direct.copy()
            membership[atom_indices] = -1
            membership = compact(membership)

        group_index = self.topology.n_groups
        self.topology.groups.loc[group_index, "group_id"] = (
            self._normalize_optional_string(group_id, default=str(group_index))
        )
        self.topology.groups.loc[group_index, "group_name"] = (
            self._normalize_optional_string(group_name, default="UNK")
        )
        if group_type is None:
            self.topology.groups.loc[group_index, "group_type"] = pd.NA
        else:
            self.topology.groups.loc[group_index, "group_type"] = str(group_type)
        self.topology.groups.loc[group_index, "molecule_index"] = molecule_index
        self.topology.atoms.loc[atom_indices, "group_index"] = int(group_index)
        self.topology._atom_molecule_membership = membership

        return group_index

    @signal(tags=["native", "builder"])
    @arg_digest()
    def add_bond(
        self,
        atom_index_1,
        atom_index_2,
        bond_order=None,
        bond_type=None,
        skip_digestion=False,
        *,
        chemical_state="reference",
    ):
        """Adding a bond between two declared atoms.

        Parameters
        ----------
        atom_index_1 : int
            Index of the first bonded atom.
        atom_index_2 : int
            Index of the second bonded atom.
        bond_order : str, int or float, optional
            Formal or fractional bond order. The legacy labels ``single``,
            ``double``, ``triple``, ``quadruple``, and ``aromatic`` are
            normalized into their dedicated chemical fields.
        bond_type : str, optional
            Chemical relationship kind: ``covalent``, ``dative``, or
            explicitly ``unknown``. Legacy order labels supplied here are
            normalized as bond order rather than retained as bond type.
        skip_digestion : bool, default False
            Whether to skip argument digestion.

        Returns
        -------
        int
            Index of the added bond after canonical bond sorting.

        Raises
        ------
        ArgumentError
            If a bond label has an unsupported type.
        StructuralInconsistencyError
            If either atom index is outside the declared topology.

        Examples
        --------
        >>> import molsysmt as msm
        >>> builder = msm.MolSysBuilder()
        >>> atom_1 = builder.add_atom(atom_name="C")
        >>> atom_2 = builder.add_atom(atom_name="O")
        >>> builder.add_bond(atom_1, atom_2, bond_order=2, bond_type="covalent")
        0

        .. versionadded:: 1.0.0
        """

        atom_indices = np.asarray([atom_index_1, atom_index_2], dtype=int)
        self._validate_existing_indices(
            atom_indices, upper_bound=self.topology.n_atoms, element_name="Bond"
        )

        state_index = self._chemical_index(chemical_state)
        self.chemical_states._append_chemical_state_bonds(
            [[int(atom_index_1), int(atom_index_2)]],
            orders=self._normalize_optional_string(bond_order, default=pd.NA),
            types=self._normalize_optional_string(bond_type, default=pd.NA),
            state_index=state_index,
        )
        self._dirty_chemical_states.add(state_index)

        endpoint_pair = sorted((int(atom_index_1), int(atom_index_2)))
        bonds = self.chemical_states._resolve_chemical_state(state_index).bonds
        matches = bonds["atom1_index"].eq(endpoint_pair[0]) & bonds["atom2_index"].eq(
            endpoint_pair[1]
        )
        return int(np.flatnonzero(matches.to_numpy())[0])

    @signal(tags=["native", "builder"])
    @arg_digest()
    def remove_bonds(
        self, bond_indices="all", skip_digestion=False, *, chemical_state="reference"
    ):
        state_index = self._chemical_index(chemical_state)
        self.chemical_states.remove_bonds(
            bond_indices, chemical_state=state_index, skip_digestion=True
        )
        self._dirty_chemical_states.add(state_index)

    @signal(tags=["native", "builder"])
    @arg_digest()
    def add_chain(
        self,
        group_indices,
        chain_id=None,
        chain_name=None,
        chain_type=None,
        allow_reassign=False,
        skip_digestion=False,
    ):
        """Adding a chain with ordered declared group membership.

        Parameters
        ----------
        group_indices : array_like of int
            Unique existing group indices, in chain order. An empty collection
            declares an empty chain. No atomic realization is required.
        chain_id : str or int, optional
            Chain label. None generates A through Z, then AA, AB and onward.
            Supplied labels are preserved as strings.
        chain_name : str, optional
            Chain name. None leaves the name unspecified until build time.
        chain_type : str, optional
            Chain type. None leaves the type available for local inference.
        allow_reassign : bool, default=False
            Whether to move already assigned groups from their previous chains.
        skip_digestion : bool, default=False
            Whether to skip MolSysMT's internal argument digestion mechanism.

        Returns
        -------
        int
            Index of the appended chain.

        Raises
        ------
        StructuralInconsistencyError
            If groups are undefined, repeated or already assigned and reassignment
            is disabled. Rejection leaves the staged chains unchanged.

        Notes
        -----
        Atom-backed membership is updated when atoms exist. Groups without atoms
        use Topology's separate compact chain/group declaration. No group-level
        chain_index column or atomic inventory is created.

        Examples
        --------
        >>> builder = MolSysBuilder()
        >>> group = builder.add_group([], group_name='ALA')
        >>> builder.add_chain([group])
        0
        >>> builder.topology.chain_groups
        ((0,),)

        .. admonition:: User guide

           See :ref:`Tutorial_Editable` for staging native hierarchy.

        .. versionadded:: 1.0.0
        """
        group_indices = self._indices_array(group_indices)
        if len(group_indices):
            self._validate_existing_indices(
                group_indices, upper_bound=self.topology.n_groups, element_name="Chain"
            )

        from molsysmt.element.chain.chain_names import _alphabetic_chain_id

        from ._chain_groups import by_chain

        membership = by_chain(self.topology)
        declared = (
            self.topology._chain_group_membership is not None
            or self.topology.n_atoms == 0
            or not len(group_indices)
            or not set(group_indices).issubset(
                set(self.topology.atoms.group_index.dropna().astype(int))
            )
        )
        if not allow_reassign and any(
            set(group_indices).intersection(groups) for groups in membership
        ):
            raise StructuralInconsistencyError(
                reason="Groups already assigned to a chain cannot be reassigned."
            )
        if not allow_reassign and "chain_index" in self.topology.atoms.columns:
            group_mask = self.topology.atoms["group_index"].isin(group_indices.tolist())
            existing = self.topology.atoms.loc[group_mask, "chain_index"]
            if len(existing) and existing.notna().any():
                raise StructuralInconsistencyError(
                    "Groups already assigned to a chain cannot be reassigned."
                )

        chain_index = self.topology.n_chains
        self.topology.chains.loc[chain_index, "chain_id"] = (
            self._normalize_optional_string(
                chain_id, default=_alphabetic_chain_id(chain_index)
            )
        )
        self.topology.chains.loc[chain_index, "chain_name"] = (
            self._normalize_optional_string(chain_name, default=pd.NA)
        )
        self.topology.chains.loc[chain_index, "chain_type"] = (
            self._normalize_optional_string(chain_type, default=pd.NA)
        )

        # chain_index lives on atoms only
        if "chain_index" not in self.topology.atoms.columns:
            self.topology.atoms["chain_index"] = pd.Series(
                pd.array([pd.NA] * self.topology.n_atoms, dtype="Int64")
            )
        for group_index in group_indices:
            atom_mask = self.topology.atoms["group_index"] == int(group_index)
            self.topology.atoms.loc[atom_mask, "chain_index"] = int(chain_index)

        if declared:
            selected = set(group_indices)
            membership = [
                [int(g) for g in groups if int(g) not in selected]
                for groups in membership
            ]
            self.topology.set_chain_groups(membership + [group_indices.tolist()])
        return chain_index

    def assign_groups_to_new_chain(
        self,
        group_indices,
        chain_id=None,
        chain_name=None,
        chain_type=None,
        skip_digestion=False,
    ):
        """Alias for ``add_chain(..., allow_reassign=True)``; allows reassigning groups already in a chain."""
        return self.add_chain(
            group_indices,
            chain_id=chain_id,
            chain_name=chain_name,
            chain_type=chain_type,
            allow_reassign=True,
            skip_digestion=skip_digestion,
        )

    @signal(tags=["native", "builder"])
    @arg_digest()
    def add_molecule(
        self,
        group_indices,
        molecule_id=None,
        molecule_name=None,
        molecule_type=None,
        skip_digestion=False,
    ):
        """Adding a declared molecule and assigning its groups.

        Parameters
        ----------
        group_indices : array_like of int
            Unique existing unassigned groups. An empty collection declares an
            empty molecule occurrence without creating atoms or bonds.
        molecule_id : str or int, optional
            Molecule label. None uses the new index, stored as a string.
        molecule_name : str, optional
            Molecule name. None leaves the name for inference during build.
        molecule_type : str, optional
            Molecule type. None leaves the type for inference during build.
        skip_digestion : bool, default=False
            Whether to skip MolSysMT's internal argument digestion mechanism.

        Returns
        -------
        int
            Index of the appended molecule.

        Raises
        ------
        StructuralInconsistencyError
            If groups are undefined, repeated or already assigned to a molecule.

        Examples
        --------
        >>> builder = MolSysBuilder()
        >>> builder.add_molecule([], molecule_name='unbuilt')
        0

        .. admonition:: User guide

           See :ref:`Tutorial_Editable` for staging native hierarchy.

        .. versionadded:: 1.0.0
        """
        group_indices = self._indices_array(group_indices)
        if len(group_indices):
            self._validate_existing_indices(
                group_indices,
                upper_bound=self.topology.n_groups,
                element_name="Molecule",
            )

        current_molecule_index = self.topology.groups.loc[
            group_indices, "molecule_index"
        ]
        if current_molecule_index.notna().any():
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                "Groups already assigned to a molecule cannot be reassigned."
            )

        molecule_index = self.topology.n_molecules
        self.topology.molecules.loc[molecule_index, "molecule_id"] = (
            self._normalize_optional_string(molecule_id, default=str(molecule_index))
        )
        self.topology.molecules.loc[molecule_index, "molecule_name"] = (
            self._normalize_optional_string(molecule_name, default=pd.NA)
        )
        self.topology.molecules.loc[molecule_index, "molecule_type"] = (
            self._normalize_optional_string(molecule_type, default=pd.NA)
        )
        self.topology.molecules.loc[molecule_index, "entity_index"] = pd.NA
        self.topology.groups.loc[group_indices, "molecule_index"] = int(molecule_index)

        return molecule_index

    @signal(tags=["native", "builder"])
    @arg_digest()
    def add_entity(
        self,
        molecule_indices,
        entity_id=None,
        entity_name=None,
        entity_type=None,
        skip_digestion=False,
    ):

        molecule_indices = self._indices_array(molecule_indices)
        self._validate_existing_indices(
            molecule_indices,
            upper_bound=self.topology.n_molecules,
            element_name="Entity",
        )

        current_entity_index = self.topology.molecules.loc[
            molecule_indices, "entity_index"
        ]
        if current_entity_index.notna().any():
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                "Molecules already assigned to an entity cannot be reassigned."
            )

        entity_index = self.topology.n_entities
        self.topology.entities.loc[entity_index, "entity_id"] = (
            self._normalize_optional_string(entity_id, default=str(entity_index))
        )
        self.topology.entities.loc[entity_index, "entity_name"] = (
            self._normalize_optional_string(entity_name, default=pd.NA)
        )
        self.topology.entities.loc[entity_index, "entity_type"] = (
            self._normalize_optional_string(entity_type, default=pd.NA)
        )
        self.topology.molecules.loc[molecule_indices, "entity_index"] = int(
            entity_index
        )

        return entity_index

    @signal(tags=["native", "builder"])
    @arg_digest()
    def set_coordinates(self, coordinates, skip_digestion=False):
        from molsysmt import pyunitwizard as puw

        value = puw.get_value(coordinates)
        if value.ndim == 2:
            value = value[np.newaxis, :, :]
            coordinates = puw.quantity(value, puw.get_unit(coordinates))
        if value.shape[1] != self.topology.n_atoms:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                "Coordinates must match the current number of atoms."
            )
        if (
            self._structure_chemical_state_indices is not None
            and len(self._structure_chemical_state_indices) != value.shape[0]
        ):
            raise StructuralInconsistencyError(
                reason="Coordinate replacement must preserve the existing structure-to-state axis.",
                caller="molsysmt.MolSysBuilder.set_coordinates",
            )
        self.structures.coordinates = coordinates

    @signal(tags=["native", "builder"])
    @arg_digest()
    def set_box(self, box, skip_digestion=False):
        from molsysmt import pyunitwizard as puw

        value = puw.get_value(box)
        if value.ndim == 2:
            value = value[np.newaxis, :, :]
            box = puw.quantity(value, puw.get_unit(box))
        if self.n_structures not in (0, value.shape[0]):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                "Box must match the current number of structures."
            )
        self.structures.box = box

    @signal(tags=["native", "builder"])
    @arg_digest()
    def set_time(self, time, skip_digestion=False):
        from molsysmt import pyunitwizard as puw

        value = puw.get_value(time)
        if value.ndim == 0:
            value = value[np.newaxis]
            time = puw.quantity(value, puw.get_unit(time))
        if self.n_structures not in (0, len(value)):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                "Time must match the current number of structures."
            )
        self.structures.time = time

    @signal(tags=["native", "builder"])
    @arg_digest()
    def set_structure_id(self, structure_id, skip_digestion=False):

        structure_id = np.asarray(structure_id)
        if structure_id.ndim == 0:
            structure_id = structure_id.reshape((1,))
        if self.n_structures not in (0, len(structure_id)):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                "Structure ids must match the current number of structures."
            )
        self.structures.structure_id = structure_id.astype(int)

    def _ensure_group_membership(self, topology):
        from ._atom_molecules import compact, stored

        direct = stored(topology)
        direct = None if direct is None else direct.copy()
        orphan_atom_indices = topology.atoms.index[
            topology.atoms["group_index"].isna()
        ].to_numpy(dtype=int)
        for atom_index in orphan_atom_indices:
            group_index = topology.n_groups
            topology.groups.loc[group_index, "group_id"] = str(group_index)
            topology.groups.loc[group_index, "group_name"] = "UNK"
            topology.groups.loc[group_index, "group_type"] = pd.NA
            topology.groups.loc[group_index, "molecule_index"] = (
                self._inherited_group_molecule(np.asarray([atom_index], dtype=np.int64))
            )
            topology.atoms.loc[atom_index, "group_index"] = int(group_index)
            if direct is not None:
                direct[atom_index] = -1
        topology._atom_molecule_membership = None if direct is None else compact(direct)

    def _fill_chain_fallbacks(self, topology):
        from molsysmt.element.chain.chain_names import _alphabetic_chain_id

        from ._chain_groups import by_chain

        membership = (
            by_chain(topology) if topology._chain_group_membership is not None else None
        )
        if topology.n_atoms == 0:
            return

        # Ensure the column exists
        if "chain_index" not in topology.atoms.columns:
            topology.atoms["chain_index"] = pd.Series(
                pd.array([pd.NA] * topology.n_atoms, dtype="Int64")
            )

        # Create chain entries for chain indices already assigned to atoms
        assigned = topology.atoms["chain_index"].dropna()
        if len(assigned) > 0:
            required_n_chains = int(assigned.astype(int).max()) + 1
            for chain_index in range(topology.n_chains, required_n_chains):
                topology.chains.loc[chain_index, "chain_id"] = _alphabetic_chain_id(
                    chain_index
                )
                topology.chains.loc[chain_index, "chain_name"] = pd.NA
                topology.chains.loc[chain_index, "chain_type"] = pd.NA

        # Any remaining unassigned atoms go into a new fallback chain
        unassigned = topology.atoms["chain_index"].isna()
        if unassigned.any():
            chain_index = topology.n_chains
            topology.chains.loc[chain_index, "chain_id"] = _alphabetic_chain_id(
                chain_index
            )
            topology.chains.loc[chain_index, "chain_name"] = pd.NA
            topology.chains.loc[chain_index, "chain_type"] = pd.NA
            topology.atoms.loc[unassigned, "chain_index"] = int(chain_index)
        if membership is not None:
            membership = [groups.tolist() for groups in membership]
            membership.extend([] for _ in range(topology.n_chains - len(membership)))
            seen = [set(groups) for groups in membership]
            for group, chain in topology.atoms[
                ["group_index", "chain_index"]
            ].itertuples(index=False, name=None):
                if (
                    not pd.isna(group)
                    and not pd.isna(chain)
                    and int(group) not in seen[int(chain)]
                ):
                    membership[int(chain)].append(int(group))
                    seen[int(chain)].add(int(group))
            topology.set_chain_groups(membership)

    def _fill_molecule_fallbacks(self, topology, chemical_states):
        if topology.n_groups == 0:
            return
        state = self._available_reference(chemical_states)
        if state is None:
            from ._topology_infer import complete_missing_molecule_membership

            complete_missing_molecule_membership(topology)
            self._fill_molecule_metadata(topology)
            return
        unassigned = topology.groups["molecule_index"].isna()
        if unassigned.any():
            # component_index is atom-level; derive per-group from atoms
            from ._chemical_components import group_components

            group_component_index = group_components(
                topology, state.component_indices.to_numpy(dtype=np.int64, na_value=-1)
            )
            unassigned_components = sorted(
                set(
                    int(group_component_index[gi])
                    for gi in topology.groups.index[unassigned]
                    if group_component_index[gi] >= 0
                )
            )
            component_to_molecule = {}
            for component_index in unassigned_components:
                molecule_index = topology.n_molecules
                topology.molecules.loc[molecule_index, "molecule_id"] = str(
                    molecule_index
                )
                topology.molecules.loc[molecule_index, "molecule_name"] = pd.NA
                topology.molecules.loc[molecule_index, "molecule_type"] = pd.NA
                topology.molecules.loc[molecule_index, "entity_index"] = pd.NA
                component_to_molecule[component_index] = molecule_index
            for group_index in topology.groups.index[unassigned]:
                ci = int(group_component_index[group_index])
                if ci < 0:
                    continue
                topology.groups.loc[group_index, "molecule_index"] = int(
                    component_to_molecule[ci]
                )

        from ._topology_infer import complete_missing_molecule_membership

        complete_missing_molecule_membership(topology)
        self._fill_molecule_metadata(topology)

    def _fill_molecule_metadata(self, topology):
        from ._topology_infer import (
            infer_molecule_names_from_topology,
            infer_molecule_types_from_topology,
        )

        topology.molecules["molecule_id"] = self._fill_missing_string_ids(
            topology.molecules["molecule_id"]
        )
        inferred_names = infer_molecule_names_from_topology(topology)
        inferred_types = infer_molecule_types_from_topology(topology)
        for molecule_index in range(topology.n_molecules):
            if pd.isna(topology.molecules.loc[molecule_index, "molecule_name"]):
                topology.molecules.loc[molecule_index, "molecule_name"] = (
                    inferred_names[molecule_index]
                )
            if pd.isna(topology.molecules.loc[molecule_index, "molecule_type"]):
                topology.molecules.loc[molecule_index, "molecule_type"] = (
                    inferred_types[molecule_index]
                )

    def _retain_group_free_molecule_axis(self, topology, chemical_states):
        """Retain declared molecules independently of the rebuilt component partition."""
        from ._atom_molecules import stored

        inherited = getattr(self, "_inherited_atom_molecules", None)
        direct = stored(topology)
        if direct is not None and (
            inherited is None or topology.n_atoms == len(inherited)
        ):
            self._fill_molecule_metadata(topology)
            return
        if inherited is None:
            if topology.n_molecules == 0:
                view = self._query_view(
                    topology=topology, chemical_states=chemical_states
                )
                view.rebuild_molecules()
            else:
                # Legacy declarative records represented their group-free axis
                # by reference components. Materialize that representation once.
                partition = chemical_states._resolve_chemical_state().component_indices
                topology.set_atom_molecules(
                    partition.to_numpy(dtype=np.int64), skip_digestion=True
                )
            return
        values = (
            np.full(topology.n_atoms, -1, dtype=np.int64)
            if direct is None
            else direct.copy()
        )
        if direct is None:
            values[: len(inherited)] = inherited
        missing = (values < 0) & (np.arange(topology.n_atoms) >= len(inherited))
        if missing.any():
            # Initial assignment of newly staged atoms uses local connectivity
            # only when it identifies an unambiguous declared owner. It never
            # changes a known owner or equates molecule and component indices.
            partition = (
                chemical_states._resolve_chemical_state().component_indices.to_numpy(
                    dtype=np.int64, na_value=-1
                )
            )
            for component in np.unique(partition[missing]):
                if component < 0:
                    continue
                members = partition == component
                owners = np.unique(values[members & ~missing])
                owners = owners[owners >= 0]
                if len(owners) == 1:
                    values[members & missing] = owners[0]
                elif not len(owners):
                    owner = topology.n_molecules
                    topology.molecules.loc[owner, "molecule_id"] = str(owner)
                    topology.molecules.loc[owner, "molecule_name"] = pd.NA
                    topology.molecules.loc[owner, "molecule_type"] = pd.NA
                    topology.molecules.loc[owner, "entity_index"] = pd.NA
                    values[members & missing] = owner
                else:
                    raise StructuralInconsistencyError(
                        caller="molsysmt.native.MolSysBuilder.build",
                        reason="New atoms connect multiple declared molecules; declare explicit groups or atom molecule ownership.",
                    )
        assignments = values.astype(object)
        assignments[values < 0] = None
        topology.set_atom_molecules(assignments, skip_digestion=True)
        self._fill_molecule_metadata(topology)

    def _fill_entity_fallbacks(self, topology):
        from ._topology_infer import (
            infer_entity_names_from_topology,
            infer_entity_types_from_topology,
        )

        unassigned = topology.molecules["entity_index"].isna()
        if unassigned.any():
            temp_topology = topology.copy()
            temp_topology.rebuild_entities(
                redefine_indices=True,
                redefine_ids=True,
                redefine_names=True,
                redefine_types=True,
            )
            fallback_entity_index = temp_topology.molecules.loc[
                unassigned, "entity_index"
            ].to_numpy(dtype=int)
            unique_fallback = sorted(set(fallback_entity_index.tolist()))
            fallback_to_declared = {}
            for fallback_index in unique_fallback:
                entity_index = topology.n_entities
                topology.entities.loc[entity_index, "entity_id"] = str(entity_index)
                topology.entities.loc[entity_index, "entity_name"] = pd.NA
                topology.entities.loc[entity_index, "entity_type"] = pd.NA
                fallback_to_declared[fallback_index] = entity_index
            for molecule_index, tmp_entity_index in zip(
                topology.molecules.index[unassigned], fallback_entity_index
            ):
                topology.molecules.loc[molecule_index, "entity_index"] = int(
                    fallback_to_declared[int(tmp_entity_index)]
                )

        topology.entities["entity_id"] = self._fill_missing_string_ids(
            topology.entities["entity_id"]
        )
        inferred_names = infer_entity_names_from_topology(topology)
        inferred_types = infer_entity_types_from_topology(topology)
        for entity_index in range(topology.n_entities):
            if pd.isna(topology.entities.loc[entity_index, "entity_name"]):
                topology.entities.loc[entity_index, "entity_name"] = inferred_names[
                    entity_index
                ]
            if pd.isna(topology.entities.loc[entity_index, "entity_type"]):
                topology.entities.loc[entity_index, "entity_type"] = inferred_types[
                    entity_index
                ]

    def _finalize_group_inventory(self, topology):
        """Complete missing hierarchy metadata without inventing atomic evidence."""
        from molsysmt.element.chain.chain_names import _alphabetic_chain_id

        from ._chain_groups import by_chain
        from ._topology_infer import (
            complete_missing_molecule_membership,
            infer_group_types_from_topology,
        )

        topology.groups["group_id"] = self._fill_missing_string_ids(
            topology.groups["group_id"]
        )
        missing = topology.groups["group_type"].isna()
        if missing.any():
            inferred = infer_group_types_from_topology(topology)
            topology.groups.loc[missing, "group_type"] = inferred[missing]
        membership = by_chain(topology)
        represented = {int(g) for groups in membership for g in groups}
        missing_groups = [g for g in range(topology.n_groups) if g not in represented]
        if missing_groups:
            chain = topology.n_chains
            topology.chains.loc[chain, "chain_id"] = _alphabetic_chain_id(chain)
            topology.chains.loc[chain, "chain_name"] = pd.NA
            topology.chains.loc[chain, "chain_type"] = pd.NA
            membership.append(missing_groups)
        topology.set_chain_groups(membership)
        complete_missing_molecule_membership(topology)
        self._fill_molecule_metadata(topology)
        for chain in range(topology.n_chains):
            if pd.isna(topology.chains.loc[chain, "chain_id"]):
                topology.chains.loc[chain, "chain_id"] = _alphabetic_chain_id(chain)
        from ._topology_infer import (
            infer_chain_names_from_topology,
            infer_chain_types_from_topology,
        )

        for column, inferred in (
            ("chain_name", infer_chain_names_from_topology(topology)),
            ("chain_type", infer_chain_types_from_topology(topology)),
        ):
            missing = topology.chains[column].isna()
            topology.chains.loc[missing, column] = inferred[missing]
        self._fill_entity_fallbacks(topology)
        topology._coerce_id_columns_to_string()
        return topology

    def _finalize_topology(self, chemical_states, *, preserve_absent_groups=False):
        topology = self.topology.copy()
        topology._coerce_id_columns_to_string()
        if topology.n_atoms == 0:
            return self._finalize_group_inventory(topology)
        if chemical_states is not None:
            for state_index in sorted(self._dirty_chemical_states):
                chemical_states.rebuild_components(
                    topology=topology, chemical_state=state_index, skip_digestion=True
                )
        if preserve_absent_groups and topology.n_groups == 0:
            self._retain_group_free_molecule_axis(topology, chemical_states)
            self._fill_entity_fallbacks(topology)
            topology._coerce_id_columns_to_string()
            return topology
        self._ensure_group_membership(topology)
        topology.groups["group_id"] = self._fill_missing_string_ids(
            topology.groups["group_id"]
        )
        if topology._chain_group_membership is None:
            topology.rebuild_groups(redefine_ids=False, redefine_types=True)
        else:
            from ._topology_infer import infer_group_types_from_topology

            missing = topology.groups["group_type"].isna()
            if missing.any():
                topology.groups.loc[missing, "group_type"] = (
                    infer_group_types_from_topology(topology)[missing]
                )
        self._fill_molecule_fallbacks(topology, chemical_states)
        self._fill_chain_fallbacks(topology)
        from molsysmt.element.chain.chain_names import _alphabetic_chain_id

        topology.chains["chain_id"] = pd.array(
            [
                _alphabetic_chain_id(index) if pd.isna(value) else str(value)
                for index, value in enumerate(topology.chains["chain_id"])
            ],
            dtype="string",
        )
        topology.rebuild_chains(
            redefine_indices=False,
            redefine_ids=False,
            redefine_names=True,
            redefine_types=True,
        )
        self._fill_entity_fallbacks(topology)
        topology._coerce_id_columns_to_string()
        return topology

    def _validate_structures(self):
        n_structures = self.n_structures
        if n_structures == 0:
            return

        if (
            self.structures.coordinates is not None
            and self.structures.coordinates.shape[1] != self.topology.n_atoms
        ):
            raise StructuralInconsistencyError(
                caller="molsysmt.native.MolSysBuilder",
                reason="Coordinates do not match the declared number of atoms.",
            )

        for attribute in ("box", "time", "structure_id"):
            values = getattr(self.structures, attribute)
            if values is not None and len(values) != n_structures:
                raise StructuralInconsistencyError(
                    caller="molsysmt.native.MolSysBuilder",
                    reason=f"{attribute} does not match the declared number of structures.",
                )

    @signal(tags=["native", "builder"])
    @arg_digest()
    def build(self, skip_digestion=False):

        return self._build(
            preserve_absent_groups=getattr(self, "_preserve_absent_groups", False)
        )

    def _build(self, *, preserve_absent_groups=False):
        """Finalize declared inventories, optionally retaining explicit group absence."""

        from .molsys import MolSys

        self._validate_structures()

        chemical_states = (
            None if self.chemical_states is None else self.chemical_states.copy()
        )
        topology = self._finalize_topology(
            chemical_states, preserve_absent_groups=preserve_absent_groups
        )
        output = MolSys._from_partial_domains(
            topology=topology,
            chemical_states=chemical_states,
            structures=self.structures.copy(),
        )
        if self._structure_chemical_state_indices is not None:
            output._set_structure_chemical_state_indices(
                self._structure_chemical_state_indices.copy()
            )
        return output

    def _chemical_index(self, chemical_state="reference"):
        if self.chemical_states is None:
            raise StructuralInconsistencyError(
                reason="Chemical editing needs an existing ChemicalStates collection; supply a state explicitly.",
                caller="molsysmt.MolSysBuilder",
            )
        return self.chemical_states._resolve_index(
            None if chemical_state in (None, "reference") else chemical_state
        )

    def _chemical_state(self, chemical_state="reference"):
        return self.chemical_states._states[self._chemical_index(chemical_state)]

    @staticmethod
    def _available_reference(chemical_states):
        if (
            chemical_states is None
            or chemical_states.reference_chemical_state_index is None
        ):
            return None
        return chemical_states._resolve_chemical_state()

    def _query_view(self, *, topology=None, chemical_states=None):
        """Borrow domain references for internal queries without copies or owner binding."""
        from .molsys import MolSys

        view = object.__new__(MolSys)
        view._topology = self.topology if topology is None else topology
        view._chemical_states_domain = (
            self.chemical_states if chemical_states is None else chemical_states
        )
        view._structures = self.structures
        view._structure_chemical_state_indices = self._structure_chemical_state_indices
        view._interactions = {}
        view.molecular_mechanics = None
        return view
