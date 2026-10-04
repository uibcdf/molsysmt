import weakref
from contextlib import contextmanager

import numpy as np
import pandas as pd
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


def _merged_bioassembly(target, source, chain_offset):
    """Merging two bioassembly catalogues, whose entries are keyed by chain index.

    Identifiers are source data and need not be unique across systems, so an incoming
    identifier that already exists is renamed rather than overwriting the target's.
    """

    if source is None:
        return target if target is None else dict(target)

    merged = {} if target is None else dict(target)
    renamed = []
    for assembly_id, assembly in source.items():
        chain_indices = assembly["chain_indices"]
        if chain_indices and isinstance(chain_indices[0], (list, tuple, np.ndarray)):
            shifted = [
                [int(index) + chain_offset for index in operation]
                for operation in chain_indices
            ]
        else:
            shifted = [int(index) + chain_offset for index in chain_indices]

        new_id = assembly_id
        suffix = 1
        while new_id in merged:
            new_id = f"{assembly_id}_{suffix}"
            suffix += 1
        if new_id != assembly_id:
            renamed.append((assembly_id, new_id))
        merged[new_id] = {**assembly, "chain_indices": shifted}

    if renamed:
        from molsysmt._private.smonitor import (
            BioassemblyIdentifierCollisionWarning,
            warn,
        )

        warn(
            BioassemblyIdentifierCollisionWarning(
                renamed=renamed, caller="molsysmt.add"
            ),
            stacklevel=2,
        )
    return merged or None


def _merged_molecular_mechanics(target, source, attribute_policy):
    """Merging two molecular-mechanics blocks along the atom axis.

    `atoms_ff` is atom-aligned, so a one-sided table would parameterize only part of the
    resulting system. A partially parameterized system is not parameterized: under the
    default policy the whole block is cleared.
    """

    from molsysmt._private.smonitor import (
        StructuralAttributeDropWarning,
        StructuralInconsistencyError,
    )

    from .molecular_mechanics import MolecularMechanics

    target_ff = None if target is None else target.atoms_ff
    source_ff = None if source is None else source.atoms_ff

    if target_ff is None and source_ff is None:
        return target.copy() if target is not None else MolecularMechanics()

    if (target_ff is None) != (source_ff is None):
        if attribute_policy == "strict":
            raise StructuralInconsistencyError(
                reason=(
                    "Only one of the two systems carries force-field parameters, so the "
                    "result would parameterize part of the atom axis; use "
                    "attribute_policy='intersection' to clear them instead"
                ),
                caller="molsysmt.native.MolSys.add",
            )
        from molsysmt._private.smonitor import warn

        warn(
            StructuralAttributeDropWarning(
                attributes=["atoms_ff"], caller="molsysmt.add"
            ),
            stacklevel=2,
        )
        return MolecularMechanics()

    merged = target.copy()
    merged.atoms_ff = pd.concat([target_ff, source_ff], ignore_index=True)
    if (
        getattr(target, "partial_charge_assignment", None) is not None
        or getattr(source, "partial_charge_assignment", None) is not None
    ):
        if attribute_policy == "strict":
            raise StructuralInconsistencyError(
                reason="Combining separate charge assignments needs an explicit joint calculation; their original provenance cannot describe the merged graph.",
                caller="molsysmt.native.MolSys.add",
            )
        from molsysmt._private.smonitor import warn

        warn(
            StructuralAttributeDropWarning(
                attributes=["partial_charge_assignment"], caller="molsysmt.add"
            ),
            stacklevel=2,
        )
        merged.partial_charge_assignment = None
    return merged


def _extend_interaction_structures(result, n_structures):
    """Preserve known observations while adding unevaluated structures."""

    if n_structures < result.n_structures:
        raise ValueError("Interaction structure axes cannot shrink during an append.")
    from .interactions_dict import _decode_interactions, _encode_interactions

    encoded = _encode_interactions(result)
    encoded.data["n_structures"] = n_structures
    if n_structures != result.n_structures:
        encoded.data["structure_source_indices"] = np.r_[
            result.structure_source_indices,
            np.full(n_structures - result.n_structures, -1, dtype=np.int64),
        ]
    return _decode_interactions(encoded)


def _extend_interaction_atoms(result, n_atoms):
    """Keep the evaluated atom universe fixed while adding new local atoms."""

    if n_atoms < result.n_atoms:
        raise ValueError("Interaction atom axes cannot shrink during an add.")
    from .interactions_dict import _decode_interactions, _encode_interactions

    encoded = _encode_interactions(result)
    encoded.data["n_atoms"] = n_atoms
    if n_atoms != result.n_atoms:
        encoded.data["atom_source_indices"] = np.r_[
            result.atom_source_indices,
            np.full(n_atoms - result.n_atoms, -1, dtype=np.int64),
        ]
        if result.evaluation_universe_indices is None:
            encoded.data["evaluation_universe_indices"] = np.arange(
                result.n_atoms, dtype=np.int64
            )
    return _decode_interactions(encoded)


class MolSys:
    """Container holding native molecular-system information domains."""

    @property
    def interactions(self):
        """Returning named interaction analyses aligned with this system."""

        from types import MappingProxyType

        analyses = getattr(self, "_interactions", {})
        self._validate_interactions(analyses)
        return MappingProxyType(analyses)

    @interactions.setter
    def interactions(self, analyses):
        """Replacing named interaction analyses after index-domain validation."""

        candidate = dict(analyses)
        self._validate_interactions(candidate)
        self._interactions = candidate

    def _validate_interactions(self, analyses):
        if not analyses:
            return

        from molsysmt.interactions.result import Interactions

        n_atoms = self._get_n_atoms()
        n_structures = None if self.structures is None else self.structures.n_structures
        for name, result in analyses.items():
            if not isinstance(name, str) or not name:
                raise ValueError("Interaction analysis names must be nonempty strings.")
            if not isinstance(result, Interactions) or not result._is_full:
                raise ValueError(
                    "Each interaction analysis must be a full Interactions result."
                )
            if n_atoms is None:
                n_atoms = result.n_atoms
            if n_structures is None:
                n_structures = result.n_structures
            if (
                n_atoms is None
                or result.n_atoms != n_atoms
                or result.n_structures != n_structures
            ):
                raise ValueError(
                    f"Interaction analysis {name!r} has atom/structure domains "
                    f"({result.n_atoms}, {result.n_structures}), expected "
                    f"({n_atoms}, {n_structures})."
                )

    @contextmanager
    def _invalidating_interaction_frames(self, structure_indices, atom_indices=None):
        """Staging frame invalidation before writes and publishing it on failure.

        The caller has validated the edit and preserved index domains.
        Once delegation starts, a failure may follow a partial write; retaining
        unevaluated frames is safer than preserving their old observations.
        """
        if not getattr(self, "_interactions", {}) or (
            atom_indices is not None
            and not is_all(atom_indices)
            and np.asarray(atom_indices).size == 0
        ):
            yield
            return
        analyses = dict(self.interactions)
        frames = (
            np.arange(self._get_n_structures(), dtype=np.int64)
            if is_all(structure_indices)
            else np.asarray(structure_indices).reshape(-1)
        )
        if frames.size == 0:
            yield
            return
        candidate = {
            name: result.invalidate_structures(frames)
            if np.isin(result.evaluated_structure_indices, frames).any()
            else result
            for name, result in analyses.items()
        }
        try:
            yield
        finally:
            self._interactions = candidate

    @property
    def topology(self):
        """Returning the stable topology and its compatibility facades."""

        return self._topology

    @topology.setter
    def topology(self, value):
        from .topology import Topology

        if not isinstance(value, Topology):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="MolSys topology must be a native Topology.",
                caller="molsysmt.native.MolSys",
            )
        owner_ref = getattr(value, "_molsys_owner_ref", None)
        owner = None if owner_ref is None else owner_ref()
        if owner is not None and owner is not self:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="A topology already attached to another MolSys must be copied.",
                caller="molsysmt.native.MolSys",
            )
        absent_chemistry = (
            "_chemical_states_domain" in self.__dict__
            and self._chemical_states_domain is None
        )
        if absent_chemistry and value._chemical_states_domain.n_chemical_states:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="A topology carrying chemical states cannot replace one with absent chemistry.",
                caller="molsysmt.native.MolSys",
            )
        association = getattr(self, "_structure_chemical_state_indices", None)
        if association is not None:
            known = pd.Series(association).dropna()
            if not known.empty and (
                absent_chemistry
                or (known >= value._chemical_states_domain.n_chemical_states).any()
            ):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason=(
                        "The structure-to-state association refers to a state "
                        "outside the replacement topology's ChemicalStates collection."
                    ),
                    caller="molsysmt.native.MolSys",
                )
        previous = getattr(self, "_topology", None)
        if previous is not None and previous is not value:
            previous._molsys_owner_ref = None
        self._topology = value
        self._chemical_states_domain = (
            None if absent_chemistry else value._chemical_states_domain
        )
        value._molsys_owner_ref = weakref.ref(self)

    @property
    def chemical_states(self):
        """Returning the independent chemical-state information domain."""

        return self._chemical_states_domain

    @chemical_states.setter
    def chemical_states(self, value):
        """Replacing chemical states and invalidating attached observations.

        A validated replacement marks every named analysis unevaluated.
        Previously held result and query snapshots remain unchanged. Editing
        a separately accessed ChemicalStates collection requires explicit
        owner invalidation; this setter does not observe its internal aliases.
        """
        from .chemical_states import ChemicalStates

        if not isinstance(value, ChemicalStates):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="MolSys chemical_states must be a ChemicalStates collection.",
                caller="molsysmt.native.MolSys",
            )
        self._replace_chemical_states(value)

    def _replace_chemical_states(self, value):
        """Keep one state authority visible through both native domains."""

        if self.topology is not None and value.n_atoms != self.topology.n_atoms:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="Chemical states and topology must share an atom-index domain.",
                caller="molsysmt.native.MolSys",
            )
        if self.structures is not None:
            payload = self.structures._frame_payload()
            if (
                any(
                    payload[name] is not None
                    for name in ("coordinates", "velocities", "b_factor", "occupancy")
                )
                and value.n_atoms != self.structures.n_atoms
            ):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason="Chemical states and structures must share an atom-index domain.",
                    caller="molsysmt.native.MolSys",
                )
        if any(
            result.n_atoms != value.n_atoms
            for result in getattr(self, "_interactions", {}).values()
        ):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="Chemical states and interactions must share an atom-index domain.",
                caller="molsysmt.native.MolSys",
            )
        value._replace_states(value._states, value._reference_index)
        association = getattr(self, "_structure_chemical_state_indices", None)
        if association is not None:
            known = pd.Series(association).dropna()
            if not known.empty and (known >= value.n_chemical_states).any():
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason=(
                        "The structure-to-state association refers to a state "
                        "outside the replacement ChemicalStates collection."
                    ),
                    caller="molsysmt.native.MolSys",
                )
        with self._invalidating_interaction_frames("all"):
            self._chemical_states_domain = value
            if self.topology is not None:
                self.topology._chemical_states_domain = value

    @signal(tags=["native"])
    @arg_digest()
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

        from .molecular_mechanics import MolecularMechanics
        from .structures import Structures
        from .topology import Topology

        self.topology = Topology(
            n_atoms=n_atoms,
            n_groups=n_groups,
            n_components=n_components,
            n_molecules=n_molecules,
            n_entities=n_entities,
            n_chains=n_chains,
            n_bonds=n_bonds,
            skip_digestion=True,
        )
        self.structures = Structures(skip_digestion=True)
        self.molecular_mechanics = MolecularMechanics()
        self._structure_chemical_state_indices = None
        self._interactions = {}

    @classmethod
    def _from_partial_domains(
        cls, *, chemical_states=None, topology=None, structures=None, interactions=None
    ):
        """Build a private partial-domain probe without inventing missing layers."""

        from .chemical_states import ChemicalStates
        from .structures import Structures
        from .topology import Topology

        if chemical_states is not None and not isinstance(
            chemical_states, ChemicalStates
        ):
            raise TypeError("chemical_states must be native ChemicalStates or None.")
        if topology is not None and not isinstance(topology, Topology):
            raise TypeError("topology must be native Topology or None.")
        if structures is not None and not isinstance(structures, Structures):
            raise TypeError("structures must be native Structures or None.")
        if (
            topology is None
            and structures is None
            and chemical_states is None
            and not interactions
        ):
            raise ValueError("A partial MolSys needs at least one information domain.")
        if chemical_states is None and topology is not None:
            if topology._chemical_states_domain.n_chemical_states:
                raise ValueError(
                    "A topology without a chemical-state layer must have no states."
                )
        if (
            topology is not None
            and chemical_states is not None
            and topology.n_atoms != chemical_states.n_atoms
        ):
            raise ValueError("Topology and chemical states must share an atom domain.")
        if structures is not None:
            payload = structures._frame_payload()
            has_atom_axis = any(
                payload[name] is not None
                for name in ("coordinates", "velocities", "b_factor", "occupancy")
            )
            if has_atom_axis:
                if (
                    chemical_states is not None
                    and structures.n_atoms != chemical_states.n_atoms
                ):
                    raise ValueError(
                        "Structures and chemical states must share an atom domain."
                    )
                if topology is not None and structures.n_atoms != topology.n_atoms:
                    raise ValueError(
                        "Structures and topology must share an atom domain."
                    )

        from .molecular_mechanics import MolecularMechanics

        result = object.__new__(cls)
        result._topology = None
        result._chemical_states_domain = chemical_states
        result.structures = structures
        result.molecular_mechanics = MolecularMechanics()
        result._structure_chemical_state_indices = None
        result._interactions = {}
        if topology is not None:
            result.topology = topology
            if chemical_states is not None:
                result.chemical_states = chemical_states
        result.interactions = {} if interactions is None else interactions
        return result

    def __setstate__(self, state):
        """Restore a molecular system and finish coordinated legacy migration."""

        legacy_topology = state.pop("topology", None)
        state.pop("_chemical_states", None)
        had_chemical_states = "_chemical_states_domain" in state
        chemical_states = state.pop("_chemical_states_domain", None)
        self.__dict__.update(state)
        if legacy_topology is not None:
            self.topology = legacy_topology
            if had_chemical_states and chemical_states is None:
                self._chemical_states_domain = None
        elif self._topology is None:
            self._chemical_states_domain = chemical_states
        else:
            self._chemical_states_domain = (
                None
                if had_chemical_states and chemical_states is None
                else self._topology._chemical_states_domain
            )
            self._topology._molsys_owner_ref = weakref.ref(self)
        if "_structure_chemical_state_indices" not in self.__dict__:
            legacy_indices = getattr(self.structures, "_chemical_state_indices", None)
            self._structure_chemical_state_indices = (
                None
                if legacy_indices is None
                else pd.array(
                    [
                        pd.NA if pd.isna(value) or int(value) < 0 else int(value)
                        for value in legacy_indices
                    ],
                    dtype="Int64",
                )
            )
        if "_interactions" not in self.__dict__:
            self._interactions = {}
        if self.structures is not None:
            self.structures.__dict__.pop("_chemical_state_indices", None)
        if self.topology is None:
            self._validate_interactions(self._interactions)
            return
        topology_formal_charge = getattr(self.topology, "_legacy_formal_charge", None)
        mechanics_formal_charge = getattr(
            self.molecular_mechanics, "_legacy_formal_charge", None
        )
        if topology_formal_charge is not None and mechanics_formal_charge is not None:
            topology_values = np.asarray(topology_formal_charge)
            mechanics_values = np.asarray(mechanics_formal_charge)
            if topology_values.shape != mechanics_values.shape or not np.array_equal(
                topology_values, mechanics_values
            ):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason=(
                        "Legacy formal charge is present with conflicting values in topology "
                        "and molecular mechanics; explicit resolution is required."
                    ),
                    caller="molsysmt.native.MolSys.__setstate__",
                )

        formal_charge = topology_formal_charge
        formal_charge_origin = "legacy_topology"
        if formal_charge is None:
            formal_charge = mechanics_formal_charge
            formal_charge_origin = "legacy_molecular_mechanics"
        if formal_charge is not None:
            self.topology._set_chemical_state_atom_attribute(
                "formal_charge", formal_charge
            )
            self.topology._reference_chemical_state._formal_charge_migration_origin = (
                formal_charge_origin
            )

        topology_partial_charge = getattr(self.topology, "_legacy_partial_charge", None)
        mechanics_partial_charge = getattr(
            self.molecular_mechanics, "_legacy_partial_charge", None
        )
        partial_charge = mechanics_partial_charge
        if partial_charge is None:
            partial_charge = topology_partial_charge
        if partial_charge is not None:
            self.molecular_mechanics.partial_charge = partial_charge

        for owner in (self.topology, self.molecular_mechanics):
            owner.__dict__.pop("_legacy_formal_charge", None)
            owner.__dict__.pop("_legacy_partial_charge", None)
        self._validate_interactions(self._interactions)

    def _get_structure_chemical_state_indices(
        self, structure_indices="all", resolved=True
    ):
        """Return explicit or implicitly resolved state indices aligned to structures."""

        if self.structures is None:
            raise ValueError("Structure-to-state associations require structures.")
        n_structures = self.structures.n_structures
        if is_all(structure_indices):
            indices = np.arange(n_structures, dtype=np.int64)
        else:
            indices = np.asarray(structure_indices, dtype=np.int64)
            if (
                indices.ndim != 1
                or np.any(indices < 0)
                or np.any(indices >= n_structures)
            ):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason="Structure indices for chemical-state association are out of range.",
                    caller="molsysmt.native.MolSys",
                )

        if self._structure_chemical_state_indices is None:
            if (
                resolved
                and self.chemical_states is not None
                and self.chemical_states.n_chemical_states == 1
            ):
                return pd.array(np.zeros(len(indices), dtype=np.int64), dtype="Int64")
            return pd.array([pd.NA] * len(indices), dtype="Int64")

        values = self._structure_chemical_state_indices[indices]
        n_states = (
            0
            if self.chemical_states is None
            else self.chemical_states.n_chemical_states
        )
        known = pd.Series(values).dropna()
        if not known.empty and ((known < 0).any() or (known >= n_states).any()):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="Structure-to-state association contains an invalid chemical-state index.",
                caller="molsysmt.native.MolSys",
            )
        return pd.array(values, dtype="Int64")

    def _set_structure_chemical_state_indices(self, values, structure_indices="all"):
        """Set nullable state indices for all or selected structures."""

        if self.structures is None:
            raise ValueError("Structure-to-state associations require structures.")
        if self.chemical_states is None and values is not None:
            raise ValueError("Structure-to-state associations require chemical states.")
        n_structures = self.structures.n_structures
        if is_all(structure_indices):
            indices = np.arange(n_structures, dtype=np.int64)
        else:
            indices = np.asarray(structure_indices, dtype=np.int64)
            if (
                indices.ndim != 1
                or np.any(indices < 0)
                or np.any(indices >= n_structures)
            ):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason="Structure indices for chemical-state association are out of range.",
                    caller="molsysmt.native.MolSys",
                )

        if values is None and is_all(structure_indices):
            with self._invalidating_interaction_frames(indices):
                self._structure_chemical_state_indices = None
            return

        if values is None or values is pd.NA:
            normalized = [pd.NA] * len(indices)
        elif np.isscalar(values):
            normalized = [values] * len(indices)
        else:
            normalized = list(values)
            if len(normalized) != len(indices):
                from molsysmt._private.smonitor import ArgumentLengthError

                raise ArgumentLengthError(
                    argument="structure_chemical_state_index",
                    expected=len(indices),
                    actual=len(normalized),
                    caller="molsysmt.native.MolSys",
                )

        array = pd.array(normalized, dtype="Int64")
        n_states = self.chemical_states.n_chemical_states
        known = pd.Series(array).dropna()
        if not known.empty and ((known < 0).any() or (known >= n_states).any()):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason=(
                    "Structure-to-state association values must reference existing "
                    "chemical-state indices."
                ),
                caller="molsysmt.native.MolSys",
            )

        if self._structure_chemical_state_indices is None:
            candidate = pd.array([pd.NA] * n_structures, dtype="Int64")
        else:
            candidate = self._structure_chemical_state_indices.copy()
        candidate[indices] = array
        with self._invalidating_interaction_frames(indices):
            self._structure_chemical_state_indices = candidate

    def _resolve_structure_chemical_state_index(self, structure_indices="all"):
        """Resolve one state shared by the requested structures or fail closed."""

        values = self._get_structure_chemical_state_indices(
            structure_indices=structure_indices, resolved=True
        )
        if len(values) == 0:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="No structures are available to resolve a chemical state.",
                caller="molsysmt.native.MolSys",
            )
        if pd.isna(values).any():
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="At least one selected structure has no chemical-state association.",
                caller="molsysmt.native.MolSys",
            )
        unique = np.unique(np.asarray(values, dtype=np.int64))
        if len(unique) != 1:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason=(
                    "The selected structures span multiple chemical states and cannot "
                    "resolve one state-dependent result."
                ),
                caller="molsysmt.native.MolSys",
            )
        return int(unique[0])

    @signal(tags=["native"])
    @arg_digest()
    def extract(
        self,
        atom_indices="all",
        structure_indices="all",
        copy_if_all=True,
        skip_digestion=False,
    ):
        """Extracting atoms and structures into a native molecular system.

        Parameters
        ----------
        atom_indices : str or array_like, default='all'
            Atom indices to retain. A topology-free system requires unique
            valid indices when this axis is selected explicitly.
        structure_indices : str or array_like, default='all'
            Structure indices to retain in the given order; repeated indices
            are allowed when a structure-index domain is declared.
        copy_if_all : bool, default=True
            Whether to return an independent copy when both selections are
            ``'all'``.
        skip_digestion : bool, default=False
            Whether to skip argument validation for a trusted internal call.

        Returns
        -------
        MolSys
            Molecular system with present domains and named interactions
            remapped to the selected index spaces.

        Raises
        ------
        ValueError
            If an explicit selection uses an absent index domain or cannot
            safely remap the available data.

        Notes
        -----
        Named interactions can declare both index domains even when the
        system has no topology or structures. For H5MSM 0.5 examples, see
        :doc:`/user/tools/form/file/h5msm_05`.
        A topology-and-chemistry system can select atoms without structures;
        absent domains stay absent. With topology, atom subsets retain the
        established sorted-index order. Without a Structures domain, explicit structure
        selection requires a structure-index domain declared by interactions.

        Examples
        --------
        >>> from molsysmt.native import MolSys
        >>> system = MolSys(n_atoms=2)
        >>> system.extract(atom_indices=[1]).get_n_atoms()
        1

        .. versionadded:: 1.0.0
        """

        if is_all(atom_indices) and is_all(structure_indices):
            if copy_if_all:
                return self.copy()
            else:
                return self

        else:
            if self.topology is None or self.structures is None:
                n_atoms = self._get_n_atoms()
                if not is_all(atom_indices):
                    if n_atoms is None:
                        raise ValueError(
                            "Atom extraction requires a declared atom-index domain."
                        )
                    atoms = np.asarray(atom_indices)
                    if atoms.size == 0:
                        atoms = np.asarray(atom_indices, dtype=np.int64)
                    if (
                        atoms.ndim != 1
                        or atoms.dtype.kind not in "iu"
                        or np.any(atoms < 0)
                        or np.any(atoms >= n_atoms)
                        or np.unique(atoms).size != atoms.size
                    ):
                        raise ValueError(
                            "atom_indices must be unique valid integer indices."
                        )
                    atom_indices = atoms.astype(np.int64, copy=False)
                    if (
                        self.topology is None
                        and self.structures is not None
                        and self.structures.bioassembly is not None
                    ):
                        raise ValueError(
                            "Atom extraction cannot remap a bioassembly without topology."
                        )
                    if self.topology is None and any(
                        value is not None
                        for value in self.molecular_mechanics.to_dict().values()
                    ):
                        raise ValueError(
                            "Atom extraction cannot remap molecular mechanics "
                            "without topology."
                        )
                    if self.topology is not None:
                        atom_indices = np.sort(atom_indices)
                if not is_all(structure_indices):
                    n_structures = self._get_n_structures()
                    if n_structures is None:
                        raise ValueError(
                            "Structure extraction requires a declared structure-index domain."
                        )
                    frames = np.asarray(structure_indices)
                    if frames.size == 0:
                        frames = np.asarray(structure_indices, dtype=np.int64)
                    if (
                        frames.ndim != 1
                        or frames.dtype.kind not in "iu"
                        or np.any(frames < 0)
                        or np.any(frames >= n_structures)
                    ):
                        raise ValueError(
                            "structure_indices must be valid integer indices."
                        )
                    structure_indices = frames.astype(np.int64, copy=False)

                topology = None
                states = None
                if self.topology is not None:
                    topology = self.topology.extract(
                        atom_indices=atom_indices,
                        copy_if_all=True,
                        skip_digestion=True,
                    )
                    if self.chemical_states is not None:
                        states = topology._chemical_states_domain
                elif self.chemical_states is not None:
                    states = (
                        self.chemical_states.copy()
                        if is_all(atom_indices)
                        else self.chemical_states._extract_atoms(atom_indices)
                    )
                extracted = MolSys._from_partial_domains(
                    topology=topology,
                    chemical_states=states,
                    structures=(
                        None
                        if self.structures is None
                        else self.structures.extract(
                            atom_indices=atom_indices,
                            structure_indices=structure_indices,
                            copy_if_all=True,
                            skip_digestion=True,
                        )
                    ),
                    interactions={
                        name: result.remap(
                            atom_indices=atom_indices,
                            structure_indices=structure_indices,
                        )
                        for name, result in self.interactions.items()
                    },
                )
                extracted.molecular_mechanics = self.molecular_mechanics.copy()
                if (
                    not is_all(atom_indices)
                    and extracted.molecular_mechanics.atoms_ff is not None
                ):
                    extracted.molecular_mechanics.atoms_ff = (
                        extracted.molecular_mechanics.atoms_ff.iloc[atom_indices]
                        .reset_index(drop=True)
                        .copy()
                    )
                if self._structure_chemical_state_indices is not None:
                    if is_all(structure_indices):
                        extracted._structure_chemical_state_indices = (
                            self._structure_chemical_state_indices.copy()
                        )
                    else:
                        extracted._structure_chemical_state_indices = pd.array(
                            self._structure_chemical_state_indices[structure_indices],
                            dtype="Int64",
                        )
                from molsysmt._private.partial_charges import project_assignment

                project_assignment(self, extracted, atom_indices)
                return extracted
            if not is_all(atom_indices):
                atom_indices = np.sort(np.asarray(atom_indices, dtype=int))

            tmp_item = MolSys()
            tmp_item.topology = self.topology.extract(
                atom_indices=atom_indices, copy_if_all=True, skip_digestion=True
            )
            tmp_item.structures = self.structures.extract(
                atom_indices=atom_indices,
                structure_indices=structure_indices,
                copy_if_all=True,
                skip_digestion=True,
            )
            if not is_all(atom_indices) and tmp_item.structures.bioassembly is not None:
                selected_chain_indices = (
                    self.topology.atoms.iloc[atom_indices]["chain_index"]
                    .dropna()
                    .astype(int)
                    .unique()
                    .tolist()
                )
                chain_index_map = {
                    old_index: new_index
                    for new_index, old_index in enumerate(selected_chain_indices)
                }
                retained_assemblies = {}
                for assembly_id, assembly in tmp_item.structures.bioassembly.items():
                    chain_indices = assembly["chain_indices"]
                    if chain_indices and isinstance(
                        chain_indices[0], (list, tuple, np.ndarray)
                    ):
                        retained_operations = [
                            operation_index
                            for operation_index, operation_chains in enumerate(
                                chain_indices
                            )
                            if all(
                                int(chain_index) in chain_index_map
                                for chain_index in operation_chains
                            )
                        ]
                        if not retained_operations:
                            continue
                        retained_assemblies[assembly_id] = {
                            **assembly,
                            "chain_indices": [
                                [
                                    chain_index_map[int(chain_index)]
                                    for chain_index in chain_indices[operation_index]
                                ]
                                for operation_index in retained_operations
                            ],
                            "rotations": assembly["rotations"][retained_operations],
                            "translations": assembly["translations"][
                                retained_operations
                            ],
                        }
                    else:
                        if not all(
                            int(chain_index) in chain_index_map
                            for chain_index in chain_indices
                        ):
                            continue
                        retained_assemblies[assembly_id] = {
                            **assembly,
                            "chain_indices": [
                                chain_index_map[int(chain_index)]
                                for chain_index in chain_indices
                            ],
                        }
                tmp_item.structures.bioassembly = retained_assemblies or None
            tmp_item.molecular_mechanics = self.molecular_mechanics.copy()
            if (
                not is_all(atom_indices)
                and tmp_item.molecular_mechanics is not None
                and tmp_item.molecular_mechanics.atoms_ff is not None
            ):
                tmp_item.molecular_mechanics.atoms_ff = (
                    tmp_item.molecular_mechanics.atoms_ff.iloc[atom_indices]
                    .reset_index(drop=True)
                    .copy()
                )
            from molsysmt._private.partial_charges import project_assignment

            project_assignment(self, tmp_item, atom_indices)
            if self._structure_chemical_state_indices is not None:
                if is_all(structure_indices):
                    tmp_item._structure_chemical_state_indices = (
                        self._structure_chemical_state_indices.copy()
                    )
                else:
                    tmp_item._structure_chemical_state_indices = pd.array(
                        self._structure_chemical_state_indices[structure_indices],
                        dtype="Int64",
                    )

            tmp_item.interactions = {
                name: result.remap(
                    atom_indices=atom_indices,
                    structure_indices=structure_indices,
                )
                for name, result in self.interactions.items()
            }

            return tmp_item

    @signal(tags=["native"])
    @arg_digest()
    def remove(
        self,
        atom_indices=None,
        structure_indices=None,
        copy_if_None=False,
        skip_digestion=False,
    ):
        """Remove atoms and/or structures by index and return the resulting MolSys."""

        if (atom_indices is None) and (structure_indices is None):
            if copy_if_None:
                return self.copy()
            else:
                return self

        else:
            if atom_indices is not None:
                atom_indices_to_be_kept = np.setdiff1d(
                    np.arange(self.topology.n_atoms), atom_indices
                )
            else:
                atom_indices_to_be_kept = "all"

            if structure_indices is not None:
                structure_indices_to_be_kept = np.setdiff1d(
                    np.arange(self.structures.n_structures), structure_indices
                )
            else:
                structure_indices_to_be_kept = "all"

            tmp_item = self.extract(
                atom_indices=atom_indices_to_be_kept,
                structure_indices=structure_indices_to_be_kept,
                skip_digestion=True,
            )

            return tmp_item

    @signal(tags=["native"])
    @arg_digest(form="molsysmt.MolSys")
    def add(
        self,
        item,
        atom_indices="all",
        structure_indices="all",
        keep_ids=True,
        attribute_policy="intersection",
        skip_digestion=False,
    ):
        """Adding topology and atom-aligned structures from another MolSys."""

        if item.interactions:
            raise ValueError(
                "Adding atoms from a source with interaction analyses "
                "requires an explicit analysis-merge policy."
            )

        n_atoms_before = self.topology.n_atoms
        n_chains_before = self.topology.n_chains

        candidate_topology = self.topology.copy()
        candidate_structures = self.structures.copy()
        candidate_topology.add(
            item.topology,
            atom_indices=atom_indices,
            keep_ids=keep_ids,
            skip_digestion=True,
        )
        n_atoms_added = candidate_topology.n_atoms - n_atoms_before
        candidate_structures.add(
            item.structures,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            attribute_policy=attribute_policy,
            n_atoms_added=n_atoms_added,
            skip_digestion=True,
        )
        candidate_structures.bioassembly = _merged_bioassembly(
            self.structures.bioassembly,
            item.structures.bioassembly,
            chain_offset=n_chains_before,
        )
        candidate_mechanics = _merged_molecular_mechanics(
            self.molecular_mechanics,
            item.molecular_mechanics,
            attribute_policy=attribute_policy,
        )
        candidate_interactions = {
            name: _extend_interaction_atoms(result, candidate_topology.n_atoms)
            for name, result in self.interactions.items()
        }

        self.topology = candidate_topology
        self.structures = candidate_structures
        self.molecular_mechanics = candidate_mechanics
        self.interactions = candidate_interactions

    @arg_digest(form="molsysmt.MolSys")
    def append_structures(
        self,
        item,
        atom_indices="all",
        structure_indices="all",
        attribute_policy="intersection",
        skip_digestion=False,
    ):
        """Append structures from another MolSys while aligning atom indices."""

        if item.interactions:
            raise ValueError(
                "Appending structures from a source with interaction analyses "
                "requires an explicit analysis merge."
            )

        source_topology = item.topology.extract(
            atom_indices=atom_indices, copy_if_all=True, skip_digestion=True
        )
        if self.topology.n_atoms != source_topology.n_atoms:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason=(
                    f"Source structures contain {source_topology.n_atoms} selected atoms, "
                    f"but the target contains {self.topology.n_atoms} atoms."
                ),
                caller="molsysmt.native.MolSys.append_structures",
            )

        inventories_match = self.topology._chemical_state_inventory_equals(
            source_topology
        )
        target_state_indices = self._get_structure_chemical_state_indices(resolved=True)
        other = item.structures.extract(
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            copy_if_all=True,
            skip_digestion=True,
        )
        if inventories_match:
            source_state_indices = item._get_structure_chemical_state_indices(
                structure_indices=structure_indices, resolved=True
            )
        elif len(self.topology._chemical_states) == 1:
            source_state_indices = pd.array(
                np.zeros(other.n_structures, dtype=np.int64), dtype="Int64"
            )
        else:
            source_state_indices = pd.array([pd.NA] * other.n_structures, dtype="Int64")
        self.structures.append(
            structure_id=other.structure_id,
            time=other.time,
            coordinates=other.coordinates,
            velocities=other.velocities,
            box=other.box,
            temperature=other.temperature,
            potential_energy=other.potential_energy,
            kinetic_energy=other.kinetic_energy,
            b_factor=other.b_factor,
            alternate_location=other.alternate_location,
            occupancy=other.occupancy,
            atom_indices="all",
            structure_indices="all",
            attribute_policy=attribute_policy,
            skip_digestion=True,
        )
        if (
            len(self.topology._chemical_states) > 1
            or self._structure_chemical_state_indices is not None
            or (
                inventories_match and item._structure_chemical_state_indices is not None
            )
        ):
            combined = pd.array(
                list(target_state_indices) + list(source_state_indices), dtype="Int64"
            )
            self._structure_chemical_state_indices = None
            self._set_structure_chemical_state_indices(combined)
        self.interactions = {
            name: _extend_interaction_structures(result, self.structures.n_structures)
            for name, result in self._interactions.items()
        }

    @signal(tags=["native"])
    def copy(self):
        """Deep-copy the MolSys."""

        if (
            self.topology is None
            or self.chemical_states is None
            or self.structures is None
        ):
            tmp_item = MolSys._from_partial_domains(
                chemical_states=(
                    None
                    if self.chemical_states is None
                    else self.chemical_states.copy()
                ),
                topology=None if self.topology is None else self.topology.copy(),
                structures=None if self.structures is None else self.structures.copy(),
                interactions={
                    name: result.remap() for name, result in self.interactions.items()
                },
            )
            tmp_item.molecular_mechanics = self.molecular_mechanics.copy()
            if self._structure_chemical_state_indices is not None:
                tmp_item._structure_chemical_state_indices = (
                    self._structure_chemical_state_indices.copy()
                )
            return tmp_item
        tmp_item = MolSys()
        tmp_item.topology = self.topology.copy()
        tmp_item.structures = self.structures.copy()
        tmp_item.molecular_mechanics = self.molecular_mechanics.copy()
        if self._structure_chemical_state_indices is not None:
            tmp_item._structure_chemical_state_indices = (
                self._structure_chemical_state_indices.copy()
            )
        tmp_item.interactions = {
            name: result.remap() for name, result in self.interactions.items()
        }
        return tmp_item

    def add_missing_bonds(
        self,
        threshold="2 angstroms",
        selection="all",
        structure_indices=0,
        syntax="MolSysMT",
        engine="MolSysMT",
        with_templates=True,
        with_distances=True,
        skip_digestion=False,
    ):
        """Fill missing bonds inferred from the current coordinates."""

        from molsysmt.build import get_missing_bonds as _get_missing_bonds

        bonds = _get_missing_bonds(
            self,
            threshold=threshold,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            engine="MolSysMT",
            with_templates=True,
            with_distances=False,
            skip_digestion=True,
        )

        self.topology.add_bonds(bonds, skip_digestion=True)

    def rebuild_atoms(self, redefine_ids=True, redefine_types=True):
        """Recompute atom ids/types from the present topology."""

        self.topology.rebuild_atoms(
            redefine_ids=redefine_ids, redefine_types=redefine_types
        )

    def rebuild_groups(self, redefine_ids=True, redefine_types=True):
        """Rebuilding group ids and group types on the native topology."""

        self.topology.rebuild_groups(
            redefine_ids=redefine_ids, redefine_types=redefine_types
        )

    def rebuild_components(self, redefine_ids=True, redefine_types=True):
        """Rebuilding component metadata on the native topology."""

        self.topology.rebuild_components(
            redefine_ids=redefine_ids, redefine_types=redefine_types
        )

    def rebuild_molecules(self, redefine_ids=True, redefine_types=True):
        """Rebuilding molecule metadata on the native topology."""

        self.topology.rebuild_molecules(
            redefine_ids=redefine_ids, redefine_types=redefine_types
        )

    def rebuild_chains(self, redefine_ids=True, redefine_types=True):
        """Recompute chain ids/types from the present topology."""

        self.topology.rebuild_chains(
            redefine_ids=redefine_ids, redefine_types=redefine_types
        )

    def rebuild_entities(self, redefine_ids=True, redefine_types=True):
        """Rebuilding entity metadata on the native topology."""

        self.topology.rebuild_entities(
            redefine_ids=redefine_ids, redefine_types=redefine_types
        )

    def to_form(self, to_form, skip_digestion=False, **kwargs):
        """Convert the MolSys to a target form."""

        from molsysmt.form import load_converter, molsysmt_MolSys

        function = load_converter(molsysmt_MolSys, molsysmt_MolSys._convert_to[to_form])

        return function(self, skip_digestion=True, **kwargs)

    def info(
        self, element="system", selection="all", syntax="MolSysMT", skip_digestion=False
    ):
        """Return a text summary of the MolSys."""

        if self.topology is None:
            raise ValueError(
                "MolSys.info requires a topology; inspect chemical_states directly."
            )

        from molsysmt.basic import info as _info

        return _info(
            self,
            element=element,
            selection=selection,
            syntax=syntax,
            skip_digestion=True,
        )

    def get(
        self,
        element="system",
        selection="all",
        structure_indices="all",
        mask=None,
        syntax="MolSysMT",
        get_missing_bonds=True,
        output_type="values",
        skip_digestion=False,
        **kwargs,
    ):
        """Proxy to :func:`molsysmt.get` using this MolSys as input."""

        from molsysmt.basic import get as _get

        return _get(
            self,
            element=element,
            selection=selection,
            structure_indices=structure_indices,
            mask=mask,
            syntax=syntax,
            get_missing_bonds=get_missing_bonds,
            output_type=output_type,
            skip_digestion=True,
            **kwargs,
        )

    def _get_n_atoms(self):
        if self.topology is not None:
            return self.topology.n_atoms
        if self.chemical_states is not None:
            return self.chemical_states.n_atoms
        if self.structures is not None:
            payload = self.structures._frame_payload()
            if any(
                payload[name] is not None
                for name in ("coordinates", "velocities", "b_factor", "occupancy")
            ):
                return self.structures.n_atoms
        analyses = getattr(self, "_interactions", {})
        if analyses:
            return next(iter(analyses.values())).n_atoms
        return None

    def _get_n_structures(self):
        if self.structures is not None:
            return self.structures.n_structures
        analyses = getattr(self, "_interactions", {})
        if analyses:
            return next(iter(analyses.values())).n_structures
        return None

    def get_n_atoms(self):
        return self._get_n_atoms()
