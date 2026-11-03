import weakref
from contextlib import contextmanager

import numpy as np
import pandas as pd
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

from .queries import NativeQueries


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
    assignments = [
        name
        for name in ("partial_charge_assignment", "atom_type_assignment")
        if getattr(target, name, None) is not None
        or getattr(source, name, None) is not None
    ]
    if assignments:
        if attribute_policy == "strict":
            raise StructuralInconsistencyError(
                reason="Combining separate mechanical assignments needs an explicit joint calculation; their original provenance cannot describe the merged graph.",
                caller="molsysmt.native.MolSys.add",
            )
        from molsysmt._private.smonitor import warn

        warn(
            StructuralAttributeDropWarning(
                attributes=assignments, caller="molsysmt.add"
            ),
            stacklevel=2,
        )
        for name in assignments:
            setattr(merged, name, None)
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


class MolSys(NativeQueries):
    """Container holding native molecular-system information domains.

    Notes
    -----
    The human-readable repr reports stored dimensions and domain presence without
    validating, copying or traversing molecular data. None means an undeclared
    axis/domain, distinct from an explicitly empty one. It is not serialization;
    use native properties or info for programmatic inspection.

    Subclasses inheriting the constructor retain its native count validation,
    including when the subclass is defined in another module. Ordinary user
    construction does not require skip_digestion.

    Examples
    --------
    >>> molsys = MolSys(n_atoms=3)
    >>> 'n_atoms=3, n_structures=0' in repr(molsys)
    True
    >>> 'n_chemical_states=1' in repr(molsys)
    True
    """

    def __repr__(self):
        """Summarizing stored metadata without reading or rendering payloads."""
        from ._repr import summary, system_fields

        return summary(self, **system_fields(self))

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
        pending = getattr(self, "_pending_interaction_edits", None)
        analyses = dict(self.interactions) if pending is None else pending["analyses"]
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
        if pending is not None:
            # Native setters may be reached inside an already staged public
            # edit. Reuse its invalidated snapshots; broader nested scopes add
            # their coverage to the same publication instead of losing it.
            pending["analyses"] = candidate
            yield
            return
        pending = {"analyses": candidate}
        self._pending_interaction_edits = pending
        try:
            yield
        finally:
            self._interactions = pending["analyses"]
            del self._pending_interaction_edits

    @property
    def structures(self):
        """Returning the structure domain whose geometry edits notify this system."""
        return self._structures

    @structures.setter
    def structures(self, value):
        """Validate shared axes and stage invalidation before attaching geometry."""
        from molsysmt._private.smonitor import StructuralInconsistencyError

        from .structures import Structures

        if value is not None and not isinstance(value, Structures):
            raise TypeError("MolSys structures must be native Structures or None.")
        previous = getattr(self, "_structures", None)
        if "_structures" in vars(self) and previous is value:
            return
        if value is not None:
            value._validate_alignment()
            size = value._atom_axis_size()
            for domain in (
                getattr(self, "_topology", None),
                getattr(self, "_chemical_states_domain", None),
            ):
                if domain is not None and size is not None and domain.n_atoms != size:
                    raise StructuralInconsistencyError(
                        reason="Replacement structures must preserve the shared atom axis.",
                        caller="molsysmt.native.MolSys.structures",
                    )
        association = getattr(self, "_structure_chemical_state_indices", None)
        if association is not None and (
            value is None or len(association) != value.n_structures
        ):
            raise StructuralInconsistencyError(
                reason="Replacement structures must preserve explicit structure-to-state associations.",
                caller="molsysmt.native.MolSys.structures",
            )
        analyses = getattr(self, "_interactions", {})
        if value is not None and any(
            result.n_structures != value.n_structures
            or value._atom_axis_size() is not None
            and result.n_atoms != value.n_atoms
            for result in analyses.values()
        ):
            raise StructuralInconsistencyError(
                reason="Replacement structures must preserve the declared interaction axes.",
                caller="molsysmt.native.MolSys.structures",
            )
        owner_ref = getattr(value, "_molsys_owner_ref", None)
        owner = None if owner_ref is None else owner_ref()
        if owner is not None and owner is not self:
            value = value.copy(deep=False)
        invalidated = {
            name: result.invalidate_structures(result.evaluated_structure_indices)
            for name, result in analyses.items()
        }
        prepared = vars(self).copy()
        prepared.update(_structures=value, _interactions=invalidated)
        if value is not None:
            value._molsys_owner_ref = weakref.ref(self)
        object.__setattr__(self, "__dict__", prepared)
        if previous is not None:
            previous._molsys_owner_ref = None

    @property
    def topology(self):
        """Returning the stable topology and its compatibility facades."""

        return self._topology

    @topology.setter
    def topology(self, value):
        from molsysmt._private.smonitor import StructuralInconsistencyError

        from .topology import Topology

        if not isinstance(value, Topology):
            raise StructuralInconsistencyError(
                reason="MolSys topology must be a native Topology.",
                caller="molsysmt.native.MolSys",
            )
        owner_ref = getattr(value, "_molsys_owner_ref", None)
        owner = None if owner_ref is None else owner_ref()
        if owner is not None and owner is not self:
            raise StructuralInconsistencyError(
                reason="A topology already attached to another MolSys must be copied.",
                caller="molsysmt.native.MolSys",
            )
        chemistry = getattr(self, "_chemical_states_domain", None)
        if chemistry is not None and chemistry.n_atoms != value.n_atoms:
            raise StructuralInconsistencyError(
                reason="Replacement topology must preserve the shared atom axis; use a coordinated molecular edit to resize it.",
                caller="molsysmt.native.MolSys",
            )
        structures = getattr(self, "_structures", None)
        if (
            structures is not None
            and structures._atom_axis_size() is not None
            and structures.n_atoms != value.n_atoms
        ):
            raise StructuralInconsistencyError(
                reason="Replacement topology and structures must share an atom axis.",
                caller="molsysmt.native.MolSys",
            )
        if any(
            result.n_atoms != value.n_atoms
            for result in getattr(self, "_interactions", {}).values()
        ):
            raise StructuralInconsistencyError(
                reason="Replacement topology and interactions must share an atom axis.",
                caller="molsysmt.native.MolSys",
            )
        previous = getattr(self, "_topology", None)
        with self._invalidating_interaction_frames("all"):
            if previous is not None and previous is not value:
                previous._molsys_owner_ref = None
            self._topology = value
            value._molsys_owner_ref = weakref.ref(self)

    def _owned_chemical_states(self, value):
        """Prepare independent chemistry when a collection has another owner."""
        owner_ref = getattr(value, "_molsys_owner_ref", None)
        owner = None if owner_ref is None else owner_ref()
        return (
            value.copy(skip_digestion=True)
            if owner is not None and owner is not self
            else value
        )

    def _bind_chemical_states(self, value):
        """Bind prepared chemistry without duplicating its topology authority."""
        previous = getattr(self, "_chemical_states_domain", None)
        if previous is not None and previous is not value:
            owner_ref = getattr(previous, "_molsys_owner_ref", None)
            if owner_ref is not None and owner_ref() is self:
                previous._molsys_owner_ref = None
        self._chemical_states_domain = value
        if value is not None:
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
        """Replace the independent chemical collection after shared-axis validation."""

        value = self._owned_chemical_states(value)
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
            self._bind_chemical_states(value)

    @signal(tags=["native"])
    @arg_digest(native_constructor="molsysmt.native.molsys.__init__")
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

        from ._chemical_state import (
            Bonds_DataFrame,
            Components_DataFrame,
            _ChemicalStateStorage,
        )
        from .chemical_states import ChemicalStates
        from .molecular_mechanics import MolecularMechanics
        from .structures import Structures
        from .topology import Topology

        self._interactions = {}
        self._structure_chemical_state_indices = None
        self._bind_chemical_states(ChemicalStates(n_atoms=n_atoms, skip_digestion=True))
        self.chemical_states._append_state(
            _ChemicalStateStorage(
                n_atoms=n_atoms,
                bonds=Bonds_DataFrame(n_bonds=n_bonds),
                components=Components_DataFrame(n_components=n_components),
            ),
            set_as_reference=True,
        )
        self.topology = Topology(
            n_atoms=n_atoms,
            n_groups=n_groups,
            n_molecules=n_molecules,
            n_entities=n_entities,
            n_chains=n_chains,
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
        if (
            topology is not None
            and chemical_states is not None
            and topology.n_atoms != chemical_states.n_atoms
        ):
            raise ValueError("Topology and chemical states must share an atom domain.")
        if structures is not None:
            if structures._atom_axis_size() is not None:
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
        elif chemical_states is not None:
            result._bind_chemical_states(result._owned_chemical_states(chemical_states))
        result.interactions = {} if interactions is None else interactions
        return result

    def __setstate__(self, state):
        """Restore a molecular system and finish coordinated legacy migration."""

        structures = state.pop("structures", state.pop("_structures", None))
        legacy_topology = state.pop("topology", None)
        state.pop("_chemical_states", None)
        had_chemical_states = "_chemical_states_domain" in state
        chemical_states = state.pop("_chemical_states_domain", None)
        self.__dict__.update(state)
        self._structures = structures
        if structures is not None:
            structures._molsys_owner_ref = weakref.ref(self)
        if legacy_topology is not None:
            self._topology = legacy_topology
        self._chemical_states_domain = chemical_states if had_chemical_states else None
        if self._topology is not None:
            self._topology._molsys_owner_ref = weakref.ref(self)
        self._bind_chemical_states(
            self._owned_chemical_states(self._chemical_states_domain)
        )
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
            self.chemical_states._set_chemical_state_atom_attribute(
                "formal_charge", formal_charge
            )
            self.chemical_states._resolve_chemical_state()._formal_charge_migration_origin = formal_charge_origin

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

        Complete stored connectivity yields components of the retained induced
        graph, independently for each chemical state. Only exact full source atom
        sets retain component labels. Partial/unavailable connectivity restricts
        declared memberships without certifying a complete graph partition.
        Molecule ownership, state ordering and structure-to-state associations
        remain independent. Stereo references are remapped or cleared when a
        defining atom is absent. Preparation histories retain their original
        operation-index scope; no chemistry is recalculated.

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
                from molsysmt._private.autodock_assignment import (
                    project_assignment as project_types,
                )

                project_types(self, extracted, atom_indices)
                return extracted
            if not is_all(atom_indices):
                atom_indices = np.sort(np.asarray(atom_indices, dtype=int))

            tmp_item = MolSys._from_partial_domains(
                topology=self.topology.extract(
                    atom_indices=atom_indices, copy_if_all=True, skip_digestion=True
                ),
                chemical_states=(
                    None
                    if self.chemical_states is None
                    else self.chemical_states.copy()
                    if is_all(atom_indices)
                    else self.chemical_states._extract_atoms(atom_indices)
                ),
                structures=self.structures.extract(
                    atom_indices=atom_indices,
                    structure_indices=structure_indices,
                    copy_if_all=True,
                    skip_digestion=True,
                ),
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
                    if len(chain_indices) and isinstance(
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
            tmp_item.molecular_mechanics = (
                None
                if self.molecular_mechanics is None
                else self.molecular_mechanics.copy()
            )
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
            from molsysmt._private.autodock_assignment import (
                project_assignment as project_types,
            )

            project_types(self, tmp_item, atom_indices)
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
        """Adding topology and atom-aligned structures from another MolSys.

        ``keep_ids`` accepts a boolean and defaults to ``True``. Native public
        calls validate arguments; leave ``skip_digestion=False`` unless every
        argument already satisfies this method's contract.
        """

        if item.interactions:
            raise ValueError(
                "Adding atoms from a source with interaction analyses "
                "requires an explicit analysis-merge policy."
            )

        n_atoms_before = self.topology.n_atoms
        n_chains_before = self.topology.n_chains

        candidate_topology = self.topology.copy()
        if self.structures is None or item.structures is None:
            if self.structures is not None or item.structures is not None:
                raise ValueError(
                    "Adding molecular systems requires compatible Structures domains or both absent."
                )
            if not is_all(structure_indices):
                raise ValueError("Structure selection requires a Structures domain.")
            candidate_structures = None
        else:
            candidate_structures = self.structures.copy(deep=False)
        candidate_topology.add(
            item.topology,
            atom_indices=atom_indices,
            keep_ids=keep_ids,
            skip_digestion=True,
        )
        from ._chemical_merge import union

        candidate_states = union(
            self.chemical_states,
            item.chemical_states,
            atom_indices,
            candidate_topology,
            keep_ids,
        )
        n_atoms_added = candidate_topology.n_atoms - n_atoms_before
        if candidate_structures is not None:
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

        from ._subset import publish_subset

        candidate = MolSys._from_partial_domains(
            topology=candidate_topology,
            chemical_states=candidate_states,
            structures=candidate_structures,
        )
        candidate.molecular_mechanics = candidate_mechanics
        if self._structure_chemical_state_indices is not None:
            candidate._structure_chemical_state_indices = (
                self._structure_chemical_state_indices.copy()
            )
        candidate.interactions = candidate_interactions
        publish_subset(self, candidate)

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

        if self.structures is None or item.structures is None:
            raise ValueError("Appending structures requires both Structures domains.")
        source_topology = (
            None
            if item.topology is None
            else item.topology.extract(
                atom_indices=atom_indices, copy_if_all=True, skip_digestion=True
            )
        )
        from ._chemical_merge import stable_inventory_equals

        source_states = item.chemical_states
        if source_states is not None and not is_all(atom_indices):
            source_states = source_states._extract_atoms(atom_indices)
        if source_states is not None:
            if (
                self.chemical_states is None
                or not self.chemical_states._inventory_equals(source_states)
                or source_topology is not None
                and not stable_inventory_equals(self.topology, source_topology)
            ):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason="Appending declared source chemistry requires exact ordered inventory alignment.",
                    caller="molsysmt.native.MolSys.append_structures",
                )
            incoming = item._get_structure_chemical_state_indices(
                structure_indices=structure_indices, resolved=True
            )
        else:
            incoming = None
        other = item.structures.extract(
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            copy_if_all=True,
            skip_digestion=True,
        )
        declared_atoms = self._get_n_atoms()
        if other._atom_axis_size() is not None and other.n_atoms != declared_atoms:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="Source and target structures must share the ordered atom axis.",
                caller="molsysmt.native.MolSys.append_structures",
            )
        self._append_structure_payload(
            structure_chemical_state_index=incoming,
            preserve_association=item._structure_chemical_state_indices is not None,
            attribute_policy=attribute_policy,
            **other._frame_payload(),
        )

    def _append_structure_payload(
        self,
        *,
        structure_chemical_state_index=None,
        preserve_association=False,
        **payload,
    ):
        """Prepare aligned structure payload and analyses before publication."""
        if self.structures is None:
            raise ValueError("Appending structures requires a Structures domain.")
        if hasattr(self, "_pending_interaction_edits"):
            raise ValueError(
                "Appending structures cannot run inside an active molecular edit."
            )
        candidate = self.structures.copy(deep=False, skip_digestion=True)
        old_count = self.structures.n_structures
        candidate.append(**payload, skip_digestion=True)
        added = candidate.n_structures - old_count
        n_states = (
            0
            if self.chemical_states is None
            else self.chemical_states.n_chemical_states
        )
        incoming = structure_chemical_state_index
        association = None
        if (
            self._structure_chemical_state_indices is not None
            or n_states > 1
            or preserve_association
            or incoming is not None
        ):
            if incoming is None:
                incoming = [0 if n_states == 1 else pd.NA] * added
            elif incoming is pd.NA or np.isscalar(incoming):
                incoming = [incoming] * added
            else:
                incoming = list(incoming)
            if len(incoming) != added:
                raise ValueError(
                    "Incoming structure-to-state indices must align with appended structures."
                )
            association = pd.array(
                list(self._get_structure_chemical_state_indices(resolved=True))
                + incoming,
                dtype="Int64",
            )
            known = pd.Series(association).dropna()
            if not known.empty and ((known < 0).any() or (known >= n_states).any()):
                raise ValueError(
                    "Incoming structure-to-state indices reference unavailable chemical states."
                )
        analyses = {
            name: _extend_interaction_structures(result, candidate.n_structures)
            for name, result in self.interactions.items()
        }
        prepared = vars(self).copy()
        prepared.update(
            _structures=candidate,
            _structure_chemical_state_indices=association,
            _interactions=analyses,
        )
        previous = self.structures
        candidate._molsys_owner_ref = weakref.ref(self)
        object.__setattr__(self, "__dict__", prepared)
        previous._molsys_owner_ref = None

    @signal(tags=["native"])
    @arg_digest()
    def copy(self, deep=True, *, skip_digestion=False):
        """Copying a molecular system with independent domain ownership.

        Parameters
        ----------
        deep : bool, default=True
            Copy coordinate/box bytes eagerly. False shares their protected
            blocks until edits replace affected blocks. Mutable tables, other
            series, named analysis handles and metadata are independent in both
            modes. Immutable sparse observation bytes may remain shared.
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        MolSys
            A copy preserving the concrete type, present domains, index spaces,
            chemical-state associations and stored analysis provenance.

        Notes
        -----
        Python copy.copy uses deferred geometry allocation; copy.deepcopy uses
        eager geometry allocation with the containing graph's memo. Copying
        invokes no native constructor, legacy migration, remapping or inference.
        Each copied domain belongs to its copied system. Its independent
        ChemicalStates collection owns chemistry; absent domains remain absent.
        Canonical tables are copied eagerly; this is not table copy-on-write.
        Repeated references to those tables follow the containing graph's memo.
        Arbitrary mutable objects in table cells and pandas metadata follow
        pandas' own copy rules, outside this molecular-data guarantee.
        Extension slots retain their declaring classes, values and aliases,
        including distinct parent and child slots with the same name.

        Coordinate and box changes through msm.set or the attached Structures
        setters invalidate the affected structures only in the edited system.
        Controlled chemical-state edits also notify the owner. Raw table/array
        writes and uncoordinated domain edits require explicit invalidation.
        Native copying does not make arbitrary external resources copyable.

        Examples
        --------
        >>> molsys = MolSys(n_atoms=2)
        >>> molsys_A = molsys.copy(deep=False)
        >>> molsys_A.topology is molsys.topology
        False
        >>> molsys_A.chemical_states is molsys.chemical_states
        False
        >>> molsys_A.chemical_states.n_atoms
        2

        .. admonition:: User guide

           See :ref:`user-foundations-molsys-copying` and :ref:`Tutorial_Copy`.

        .. versionadded:: 1.0.0
        """
        from copy import deepcopy

        if not isinstance(skip_digestion, bool):
            from molsysmt._private.argdigest.argument.skip_digestion import (
                digest_skip_digestion,
            )

            digest_skip_digestion(skip_digestion)
        return deepcopy(self) if deep else self.__copy__()

    def __copy__(self):
        """Copying independent domains over shared protected geometry blocks."""
        from ._copy import _deferred_geometry_memo

        return self.__deepcopy__(_deferred_geometry_memo(self.structures))

    def __deepcopy__(self, memo):
        """Copying the native graph and binding domains to their new owner."""
        from ._copy import _clone

        if id(self) in memo:
            return memo[id(self)]
        result = _clone(self, memo, exclude=("_pending_interaction_edits",))
        if result._topology is not None:
            result._topology._molsys_owner_ref = weakref.ref(result)
        if result.structures is not None:
            result.structures._molsys_owner_ref = weakref.ref(result)
        if result.chemical_states is not None:
            result.chemical_states._molsys_owner_ref = weakref.ref(result)
        return result

    @arg_digest()
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
        *,
        chemical_state="reference",
    ):
        """Adding missing pairs through the existing candidate tools.

        Parameters
        ----------
        threshold : quantity or str, default='2 angstroms'
            Length cutoff for geometric candidates.
        selection : str or array-like of int, default='all'
            Source atom selection; both endpoints must be selected.
        structure_indices : int or array-like of int, default=0
            Exactly one source structure used for geometric evidence.
        syntax : str, default='MolSysMT'
            Syntax used to resolve selection.
        engine : str, default='MolSysMT'
            Existing candidate engine, forwarded without substitution.
        with_templates : bool, default=True
            Include candidates from available intra-group templates.
        with_distances : bool, default=True
            Include the existing distance-based candidate families.
        skip_digestion : bool, default=False
            Skip argument digestion only for validated inputs.
        chemical_state : str or int, default='reference'
            Existing state to edit; 'structure' resolves the selected structure.

        Returns
        -------
        None
            Add validated candidates and rebuild selected-state components.
            Other states and the stable molecular inventory remain unchanged.

        Notes
        -----
        Candidate heuristics do not certify complete connectivity. This method
        delegates to build.get_missing_bonds and ChemicalStates.add_bonds; it
        does not add a second chemical store or infer a missing chemical state.

        .. versionadded:: 1.0.0
        """
        from molsysmt._private.smonitor import (
            ArgumentError,
            StructuralInconsistencyError,
        )
        from molsysmt.build import get_missing_bonds

        frames = np.asarray(structure_indices).reshape(-1)
        if len(frames) != 1 or not np.issubdtype(frames.dtype, np.integer):
            raise ArgumentError(
                "structure_indices",
                value=structure_indices,
                caller="molsysmt.MolSys.add_missing_bonds",
            )
        if self.chemical_states is None:
            raise StructuralInconsistencyError(
                reason="Missing-bond preparation requires an existing ChemicalStates domain.",
                caller="molsysmt.MolSys.add_missing_bonds",
            )
        state = (
            self._resolve_structure_chemical_state_index([int(frames[0])])
            if chemical_state == "structure"
            else chemical_state
        )
        bonds = get_missing_bonds(
            self,
            selection=selection,
            structure_index=int(frames[0]),
            max_bond_length=threshold,
            syntax=syntax,
            engine=engine,
            with_templates=with_templates,
            with_distances=with_distances,
            chemical_state=state,
        )
        self.chemical_states.add_bonds(bonds, chemical_state=state)

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

    @arg_digest(native_chemical_rebuild=True, native_chemical_state=True)
    def rebuild_components(
        self,
        redefine_ids=True,
        redefine_types=True,
        *,
        redefine_indices=True,
        redefine_names=True,
        force=False,
        chemical_state="reference",
        skip_digestion=False,
    ):
        """Rebuilding selected-state components with explicit stable context.

        Parameters
        ----------
        redefine_ids : bool, default=True
            Generate local component IDs instead of retaining exact-set labels.
        redefine_types : bool, default=True
            Infer types from represented stable groups where evidence is available.
        redefine_indices : bool, default=True
            Recompute the partition from stored bonds and participation declarations.
        redefine_names : bool, default=True
            Infer names from represented stable groups.
        force : bool, default=False
            Recompute membership even when redefine_indices is False.
        chemical_state : str, int or None, default='reference'
            Existing state to rebuild without changing its reference.
        skip_digestion : bool, default=False
            Skip digestion only for already validated arguments.

        Returns
        -------
        None
            Publish the validated chemical edit, preserving stable inventory.

        .. versionadded:: 1.0.0
        """
        if self.chemical_states is None:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="Component reconstruction requires ChemicalStates.",
                caller="molsysmt.MolSys.rebuild_components",
            )
        self.chemical_states.rebuild_components(
            redefine_indices,
            redefine_ids,
            redefine_types,
            redefine_names,
            force,
            chemical_state=chemical_state,
            topology=self.topology,
            skip_digestion=True,
        )

    def rebuild_molecules(self, redefine_ids=True, redefine_types=True):
        """Rebuilding molecule metadata on the native topology."""

        from ._atom_molecules import stored

        topology = self.topology
        if (
            topology.n_atoms
            and topology.n_groups == 0
            and stored(topology) is None
            and self.chemical_states is not None
        ):
            state = self.chemical_states._resolve_chemical_state()
            topology.reset_molecules(n_molecules=len(state.components))
            topology.molecules["molecule_name"] = state.components[
                "component_name"
            ].to_numpy(copy=True)
            topology.molecules["molecule_type"] = state.components[
                "component_type"
            ].to_numpy(copy=True)
            topology.set_atom_molecules(
                state.component_indices.to_numpy(dtype=np.int64, na_value=-1),
                skip_digestion=True,
            )
        topology.rebuild_molecules(
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
        """Converting this system through its registered form adapter.

        Parameters
        ----------
        to_form : str
            Registered target form name, such as 'molsysmt.Structures'.
        skip_digestion : bool, default=False
            Whether to skip argument digestion for already validated inputs.
        **kwargs
            Options accepted by the selected converter, such as atom_indices,
            structure_indices and, where supported, copy_if_all. These indices
            are positions on this system's axes, not element IDs.

        Returns
        -------
        object
            The selected converter's result in the requested form.

        Raises
        ------
        ArgumentError
            If an option is invalid under the selected converter's contract.
        KeyError
            If the target form is not registered for MolSys conversion.

        Notes
        -----
        The registered adapter provides argument validation and normalization.
        This convenience method forwards the caller's skip_digestion flag;
        it does not assume that user input has already been checked. Selection
        and copy behavior follow the adapter. No conversion is inferred from
        output filenames; use molsysmt.convert for that public workflow.

        See Also
        --------
        molsysmt.basic.convert : Converting supported molecular-system forms.

        Examples
        --------
        >>> from molsysmt.native import MolSys
        >>> molsys = MolSys(n_atoms=2)
        >>> copied = molsys.to_form('molsysmt.MolSys')
        >>> copied is molsys
        False
        >>> copied.get(n_atoms=True)
        2

        .. admonition:: User guide

           See :ref:`Tutorial_Convert` for conversion and selection semantics.

        .. versionadded:: 1.0.0
        """

        from molsysmt.form import load_converter, molsysmt_MolSys

        function = load_converter(molsysmt_MolSys, molsysmt_MolSys._convert_to[to_form])

        return function(self, skip_digestion=skip_digestion, **kwargs)

    def _get_n_atoms(self):
        if self.topology is not None:
            return self.topology.n_atoms
        if self.chemical_states is not None:
            return self.chemical_states.n_atoms
        if self.structures is not None:
            n_atoms = self.structures._atom_axis_size()
            if n_atoms is not None:
                return n_atoms
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
