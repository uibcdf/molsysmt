from copy import deepcopy

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentLengthError,
    NotImplementedMethodError,
    StructuralInconsistencyError,
    warn,
)
from molsysmt._private.variables import is_all

from ._structure_array import _StructureArray
from .queries import NativeQueries


def _raw_value(quantity, canonical_unit):
    if quantity is None:
        return None
    if puw.is_quantity(quantity):
        return puw.get_value(quantity, to_unit=canonical_unit)
    return quantity


_FRAME_ATTRIBUTES = (
    "structure_id",
    "time",
    "coordinates",
    "velocities",
    "box",
    "b_factor",
    "alternate_location",
    "occupancy",
    "temperature",
    "potential_energy",
    "kinetic_energy",
)

_ATOM_ALIGNED_ATTRIBUTES = (
    "coordinates",
    "velocities",
    "b_factor",
    "occupancy",
)

# These describe the system as a whole rather than one atom or one structure. Adding
# atoms changes the system they describe, so they cannot survive the operation.
_SYSTEM_LEVEL_OBSERVABLES = (
    "temperature",
    "potential_energy",
    "kinetic_energy",
)

_BOX_TOLERANCE_NM = 1e-6


def _box_mismatch_reason(target_box, source_box):
    """Returning why two periodic boxes disagree, or None when they are compatible."""

    if target_box is None and source_box is None:
        return None
    if target_box is None:
        return "the target system has no periodic box while the added atoms do"
    if source_box is None:
        return "the added atoms have no periodic box while the target system does"

    target = np.asarray(target_box, dtype=float)
    source = np.asarray(source_box, dtype=float)
    if target.shape != source.shape:
        return f"box shapes differ, {target.shape} against {source.shape}"
    if np.allclose(target, source, atol=_BOX_TOLERANCE_NM, rtol=0.0):
        return None
    structure = int(
        np.argmax(np.abs(target - source).reshape(target.shape[0], -1).max(axis=1))
    )
    return (
        f"the boxes differ, first at structure {structure}: "
        f"{np.diag(target[structure])} against {np.diag(source[structure])} nm"
    )


def _remap_alternate_atom_indices(value, atom_indices):
    """Move already-selected sparse keys to the selected local atom domain."""
    if value is None or is_all(atom_indices):
        return value
    index_map = {int(old): new for new, old in enumerate(atom_indices)}
    remapped = [
        {
            index_map[int(old)]: entry
            for old, entry in sites.items()
            if int(old) in index_map
        }
        if isinstance(sites, dict)
        else deepcopy(sites)
        for sites in value
    ]
    if isinstance(value, np.ndarray):
        return np.asarray(remapped, dtype=value.dtype)
    return remapped


def _merge_alternate_locations(target_value, source_value, atom_offset, n_structures):
    """Merging two alternate-location series, whose keys are atom indices.

    The series is stored per structure but its content is keyed by atom index, so the
    incoming keys have to move by the size of the target's atom axis.
    """

    if source_value is None:
        return target_value

    def _entries(value):
        if value is None:
            return [{} for _ in range(n_structures)]
        return list(value)

    target_entries = _entries(target_value)
    source_entries = list(source_value)
    if len(target_entries) != len(source_entries):
        return target_value

    merged = []
    for target_entry, source_entry in zip(target_entries, source_entries):
        if not isinstance(target_entry, dict) or not isinstance(source_entry, dict):
            # Only the documented dict shape can be remapped; anything else keeps the
            # target's entry rather than being silently reinterpreted.
            merged.append(target_entry)
            continue
        combined = dict(target_entry)
        combined.update(
            {int(index) + atom_offset: value for index, value in source_entry.items()}
        )
        merged.append(combined)
    return merged


class Structures(NativeQueries):
    """Storing per-structure data (coordinates, box, time, energies) for a molecular system.

    Notes
    -----
    The human-readable repr uses stored shape metadata, without validating or
    formatting arrays or quantities. n_atoms=None means no atom-aligned series
    declares that axis; it is distinct from an explicit zero-length atom axis.

    Examples
    --------
    >>> repr(Structures())
    'Structures(n_atoms=None, n_structures=0, coordinates=False, box=False)'
    """

    def __repr__(self):
        """Summarizing stored metadata without reading or rendering payloads."""
        from ._repr import structure_dimensions, summary

        n_structures, n_atoms = structure_dimensions(self)
        return summary(
            self,
            n_atoms=n_atoms,
            n_structures=n_structures,
            coordinates=vars(self).get("_coordinates") is not None,
            box=vars(self).get("_box") is not None,
        )

    @property
    def time_step(self):
        if self._time_step is None:
            return None
        return puw.quantity(self._time_step, "ps")

    @time_step.setter
    def time_step(self, value):
        self._time_step = _raw_value(value, "ps")

    @property
    def time(self):
        if self._time is None:
            return None
        return puw.quantity(self._time, "ps")

    @time.setter
    def time(self, value):
        self._time = _raw_value(value, "ps")

    @property
    def coordinates(self):
        if self._coordinates is None:
            return None
        return puw.quantity(self._coordinates._dense(), "nm")

    @coordinates.setter
    def coordinates(self, value):
        val = _raw_value(value, "nm")
        candidate = (
            val._fork()
            if isinstance(val, _StructureArray)
            else None
            if val is None
            else _StructureArray(val)
        )
        self._publish_geometry("coordinates", candidate)

    @property
    def velocities(self):
        if self._velocities is None:
            return None
        return puw.quantity(self._velocities, "nm/ps")

    @velocities.setter
    def velocities(self, value):
        self._velocities = _raw_value(value, "nm/ps")

    @property
    def box(self):
        if self._box is None:
            return None
        return puw.quantity(self._box._dense(), "nm")

    @box.setter
    def box(self, value):
        val = _raw_value(value, "nm")
        candidate = (
            val._fork()
            if isinstance(val, _StructureArray)
            else None
            if val is None
            else _StructureArray(val)
        )
        self._publish_geometry("box", candidate)

    def _publish_geometry(
        self, name, candidate, structure_indices="all", atom_indices=None
    ):
        """Publish prepared geometry and its owner's invalidation together."""
        if candidate is getattr(self, "_" + name):
            return
        if name == "box" and candidate is not None and candidate.shape[1:] != (3, 3):
            raise StructuralInconsistencyError(
                reason="Periodic boxes must have shape (n_structures, 3, 3).",
                caller="molsysmt.native.Structures",
            )
        owner_ref = getattr(self, "_molsys_owner_ref", None)
        owner = None if owner_ref is None else owner_ref()
        if owner is None:
            setattr(self, "_" + name, candidate)
            return
        # Builders may populate a fresh domain in stages. Once analyses exist,
        # geometry edits must preserve their declared axes and series alignment.
        if getattr(owner, "_interactions", {}):
            payload = self._frame_payload()
            payload[name] = candidate
            n_structures, n_atoms = self._payload_dimensions(
                payload, caller="molsysmt.native.Structures"
            )
            if any(
                result.n_structures != n_structures
                or (
                    name == "coordinates"
                    and candidate is not None
                    and result.n_atoms != n_atoms
                )
                for result in owner._interactions.values()
            ):
                raise StructuralInconsistencyError(
                    reason="Geometry edits cannot resize axes with attached interactions; use extraction or append_structures.",
                    caller="molsysmt.native.Structures",
                )
        with owner._invalidating_interaction_frames(
            structure_indices, atom_indices=atom_indices
        ):
            setattr(self, "_" + name, candidate)

    @property
    def b_factor(self):
        if self._b_factor is None:
            return None
        return puw.quantity(self._b_factor, "nm**2")

    @b_factor.setter
    def b_factor(self, value):
        self._b_factor = _raw_value(value, "nm**2")

    @property
    def occupancy(self):
        if self._occupancy is None:
            return None
        return self._occupancy

    @occupancy.setter
    def occupancy(self, value):
        self._occupancy = value

    @property
    def temperature(self):
        if self._temperature is None:
            return None
        return puw.quantity(self._temperature, "K")

    @temperature.setter
    def temperature(self, value):
        self._temperature = _raw_value(value, "K")

    @property
    def potential_energy(self):
        if self._potential_energy is None:
            return None
        return puw.quantity(self._potential_energy, "kJ/mol")

    @potential_energy.setter
    def potential_energy(self, value):
        self._potential_energy = _raw_value(value, "kJ/mol")

    @property
    def kinetic_energy(self):
        if self._kinetic_energy is None:
            return None
        return puw.quantity(self._kinetic_energy, "kJ/mol")

    @kinetic_energy.setter
    def kinetic_energy(self, value):
        self._kinetic_energy = _raw_value(value, "kJ/mol")

    @property
    def n_structures(self):
        n_structures, _ = self._validate_alignment()
        return n_structures

    @property
    def n_atoms(self):
        _, n_atoms = self._validate_alignment()
        return n_atoms

    @signal(tags=["native"])
    @arg_digest(structure_series=True)
    def __init__(
        self,
        constant_time_step=False,
        time_step=None,
        constant_id_step=False,
        id_step=None,
        constant_box=False,
        structure_id=None,
        time=None,
        coordinates=None,
        velocities=None,
        box=None,
        b_factor=None,
        alternate_location=None,
        bioassembly=None,
        temperature=None,
        potential_energy=None,
        kinetic_energy=None,
        occupancy=None,
        skip_digestion=False,
    ):
        """Constructing aligned coordinate structures and optional observables.

        Parameters
        ----------
        constant_time_step : bool, default=False
            Whether a constant time step is declared. Explicit series must still align.
        time_step : quantity, optional
            Declared time increment, with time units such as ps.
        constant_id_step : bool, default=False
            Whether a constant structure-label increment is declared.
        id_step : int, optional
            Declared increment between structure labels.
        constant_box : bool, default=False
            Whether a constant periodic box is declared. Explicit series must still align.
        structure_id : array-like, optional
            Structure labels, shape (n_structures,); distinct from positional indices.
        time : quantity, optional
            Time values, shape (n_structures,), with time units such as ps.
        coordinates : quantity, optional
            Cartesian coordinates, shape (n_structures, n_atoms, 3), with length units.
            A single structure may use shape (n_atoms, 3). Internal lengths are in nm.
        velocities : quantity, optional
            Atomic velocities, shape (n_structures, n_atoms, 3), with length/time units.
        box : quantity, optional
            Periodic box vectors in rows, shape (n_structures, 3, 3), with length units.
        b_factor : quantity, optional
            Atomic B-factors, shape (n_structures, n_atoms), with length-squared units.
        alternate_location : sequence of dict, optional
            Sparse alternate-site mappings on the atom axis, one mapping per structure.
        bioassembly : dict, optional
            Mapping of assembly names to operation dictionaries, stored separately
            from aligned series. Each dictionary contains proper rotation matrices
            ``rotations`` of shape (n_operations, 3, 3), unit-bearing length
            ``translations`` of shape (n_operations, 3), and ``chain_indices``.
            Chain indices are a common integer sequence or one sequence per
            operation. Translations also accept a list of unit-bearing vectors.
            Validation does not modify the supplied mapping.
        temperature : quantity, optional
            One temperature per structure, shape (n_structures,), with temperature units.
            A scalar represents one structure and becomes a length-one series.
        potential_energy : quantity, optional
            Potential energy per structure, shape (n_structures,), with energy/mole units.
            A scalar becomes a length-one series. Internal values use kJ/mol.
        kinetic_energy : quantity, optional
            Kinetic energy per structure, shape (n_structures,), with energy/mole units.
            A scalar becomes a length-one series. Internal values use kJ/mol.
        occupancy : array-like, optional
            Dimensionless atomic occupancies, shape (n_structures, n_atoms).
        skip_digestion : bool, default=False
            Whether to skip argument digestion for already normalized internal inputs.

        Raises
        ------
        ArgumentError
            If an observable lacks compatible units, is not real-valued, or has rank > 1.
        StructuralInconsistencyError
            If supplied structure/atom axes disagree or stored observable ranks are invalid.

        Notes
        -----
        Observable values require explicit units. Omitted observables remain None.
        Empty series represent zero structures; a scalar is never broadcast across
        several coordinate structures. Temperature is stored in K and energies in
        kJ/mol; get() standardizes quantities using the active unit policy.
        Neither coordinates nor topology are required for an observable-only object.

        Examples
        --------
        >>> from molsysmt import pyunitwizard as puw
        >>> from molsysmt.native import Structures
        >>> molsys = Structures(temperature=puw.quantity([300000., 301000.], 'mK'))
        >>> molsys.n_structures
        2
        >>> puw.get_value(molsys.get(temperature=True), to_unit='K').tolist()
        [300.0, 301.0]

        .. versionadded:: 1.0.0
        """

        self._time_step = None
        self._time = None
        self._coordinates = None
        self._velocities = None
        self._box = None
        self._b_factor = None
        self._occupancy = None
        self._temperature = None
        self._potential_energy = None
        self._kinetic_energy = None

        self.constant_time_step = constant_time_step
        self.time_step = time_step
        self.constant_id_step = constant_id_step
        self.id_step = id_step
        self.constant_box = constant_box

        self.structure_id = structure_id
        self.time = time
        self.coordinates = coordinates
        self.velocities = velocities
        self.box = box
        self.b_factor = b_factor
        self.alternate_location = alternate_location
        self.bioassembly = bioassembly
        self.temperature = temperature
        self.potential_energy = potential_energy
        self.kinetic_energy = kinetic_energy
        self.occupancy = occupancy
        self._validate_alignment()

    def _frame_payload(self):
        """Returning raw frame-aligned storage without unit wrappers."""

        return {
            "structure_id": self.structure_id,
            "time": self._time,
            "coordinates": self._coordinates,
            "velocities": self._velocities,
            "box": self._box,
            "b_factor": self._b_factor,
            "alternate_location": self.alternate_location,
            "occupancy": self._occupancy,
            "temperature": self._temperature,
            "potential_energy": self._potential_energy,
            "kinetic_energy": self._kinetic_energy,
        }

    @staticmethod
    def _payload_dimensions(payload, caller, payload_error=False):
        """Validating shared structure and atom axes for one payload."""

        for name in _SYSTEM_LEVEL_OBSERVABLES:
            value = payload.get(name)
            if value is not None and np.ndim(value) != 1:
                raise StructuralInconsistencyError(
                    reason=f"Structural observable {name!r} must have one value per structure in a one-dimensional array.",
                    caller=caller,
                )

        lengths = {
            name: len(value) for name, value in payload.items() if value is not None
        }
        if lengths:
            expected_name, expected = next(iter(lengths.items()))
            for name, actual in lengths.items():
                if actual != expected:
                    if payload_error:
                        raise ArgumentLengthError(
                            argument=name,
                            expected=expected,
                            actual=actual,
                            caller=caller,
                        )
                    raise StructuralInconsistencyError(
                        reason=(
                            f"Structural series {expected_name!r} has {expected} "
                            f"entries while {name!r} has {actual}."
                        ),
                        caller=caller,
                    )
            n_structures = expected
        else:
            n_structures = 0

        atom_sizes = {}
        for name in _ATOM_ALIGNED_ATTRIBUTES:
            value = payload.get(name)
            if value is None:
                continue
            shape = getattr(value, "shape", None)
            if shape is None:
                shape = np.asarray(value).shape
            if len(shape) < 2:
                raise StructuralInconsistencyError(
                    reason=f"Structural attribute {name!r} has no atom axis.",
                    caller=caller,
                )
            atom_sizes[name] = shape[1]

        if atom_sizes:
            expected_name, expected = next(iter(atom_sizes.items()))
            for name, actual in atom_sizes.items():
                if actual != expected:
                    raise StructuralInconsistencyError(
                        reason=(
                            f"Atom axis for {expected_name!r} has size {expected} "
                            f"while {name!r} has size {actual}."
                        ),
                        caller=caller,
                    )
            n_atoms = expected
        else:
            n_atoms = 0

        return n_structures, n_atoms

    def _validate_alignment(self):
        """Validating and returning the native structure and atom dimensions."""

        return self._payload_dimensions(
            self._frame_payload(),
            caller="molsysmt.native.Structures",
        )

    def _assign_frame_payload(self, payload):
        """Preparing owned raw series before publishing a validated replacement."""
        self._payload_dimensions(payload, caller="molsysmt.native.Structures")
        candidate = {}
        for name in _FRAME_ATTRIBUTES:
            value = payload.get(name)
            if name in {"coordinates", "box"}:
                if isinstance(value, _StructureArray):
                    value = value._fork(deep=True)
                elif value is not None:
                    value = _StructureArray(_raw_value(value, "nm"))
            else:
                value = deepcopy(value)
            key = name if name in {"structure_id", "alternate_location"} else "_" + name
            candidate[key] = value
        self.__dict__.update(candidate)

    def __setstate__(self, state):
        """Restore current storage or migrate legacy public array fields."""

        restored = type(self)(skip_digestion=True)
        self.__dict__.update(restored.__dict__)
        if "_coordinates" in state:
            self.__dict__.update(state)
            for name in ("_coordinates", "_box"):
                value = getattr(self, name)
                if value is not None and not isinstance(value, _StructureArray):
                    setattr(self, name, _StructureArray(value))
            return

        legacy_fields = {
            "time",
            "coordinates",
            "velocities",
            "box",
            "b_factor",
            "occupancy",
            "temperature",
            "potential_energy",
            "kinetic_energy",
        }
        for field in legacy_fields:
            if field in state:
                setattr(self, field, state[field])
        for key, value in state.items():
            if key not in legacy_fields and key not in {"n_atoms", "n_structures"}:
                self.__dict__[key] = value

    def __getstate__(self):
        """Exclude the weak owner link from standalone and enclosing serialization."""
        return {
            key: value
            for key, value in vars(self).items()
            if key != "_molsys_owner_ref"
        }

    @signal(tags=["native"])
    @arg_digest(structure_series=True)
    def append(
        self,
        structure_id=None,
        time=None,
        coordinates=None,
        velocities=None,
        box=None,
        temperature=None,
        potential_energy=None,
        kinetic_energy=None,
        b_factor=None,
        alternate_location=None,
        occupancy=None,
        atom_indices="all",
        structure_indices="all",
        attribute_policy="intersection",
        skip_digestion=False,
    ):
        """Appending selected structures and their aligned metadata.

        Parameters
        ----------
        structure_id : array-like, optional
            Labels for the incoming structures, distinct from positional indices.
        time : quantity, optional
            Incoming time series, shape (n_structures,), with time units such as ps.
        coordinates : quantity, optional
            Incoming coordinates, shape (n_structures, n_atoms, 3), with length units.
        velocities : quantity, optional
            Incoming velocities, shape (n_structures, n_atoms, 3), with length/time units.
        box : quantity, optional
            Box vectors in rows, shape (n_structures, 3, 3), with length units.
        temperature : quantity, optional
            Incoming temperatures, shape (n_structures,), with temperature units.
            A scalar becomes a length-one series and is not broadcast.
        potential_energy : quantity, optional
            Incoming potential energies, shape (n_structures,), with energy/mole units.
            A scalar becomes a length-one series. Internal values use kJ/mol.
        kinetic_energy : quantity, optional
            Incoming kinetic energies, shape (n_structures,), with energy/mole units.
            A scalar becomes a length-one series. Internal values use kJ/mol.
        b_factor : quantity, optional
            Incoming atomic B-factors, shape (n_structures, n_atoms), with length-squared units.
        alternate_location : sequence of dict, optional
            Sparse alternate-site mappings, one mapping per incoming structure.
        occupancy : array-like, optional
            Incoming dimensionless occupancies, shape (n_structures, n_atoms).
        atom_indices : str or list of int, default='all'
            Incoming atom positions to append. The default includes every incoming atom.
        structure_indices : str or list of int, default='all'
            Incoming structure positions to append, preserving order and repetitions.
        attribute_policy : {'intersection', 'strict'}, default='intersection'
            Keep shared series and warn when dropping one-sided series, or reject
            one-sided series under strict policy. An empty target adopts the incoming data.
        skip_digestion : bool, default=False
            Whether to skip argument digestion for already normalized internal inputs.

        Returns
        -------
        None
            The receiver is updated in place.

        Raises
        ------
        ArgumentError
            If observable units, numeric types or ranks are invalid, or policy is unknown.
        ArgumentLengthError
            If incoming structure-series lengths or the target/incoming atom counts disagree.
        StructuralInconsistencyError
            If stored series are malformed or strict policy refuses one-sided attributes.

        Notes
        -----
        Observable quantities follow the constructor's one-dimensional contract.
        Compatible units are converted before storage; get() follows the active
        output unit policy. Invalid units, ranks and axis lengths are rejected
        before changing the stored series. Existing attribute-policy semantics
        also apply to temperature and energy observables.

        Examples
        --------
        >>> from molsysmt import pyunitwizard as puw
        >>> from molsysmt.native import Structures
        >>> molsys = Structures(temperature=puw.quantity([300., 301.], 'K'))
        >>> molsys.append(temperature=puw.quantity(302000., 'mK'))
        >>> puw.get_value(molsys.get(temperature=True), to_unit='K').tolist()
        [300.0, 301.0, 302.0]

        .. versionadded:: 1.0.0
        """

        if attribute_policy not in {"intersection", "strict"}:
            from molsysmt._private.smonitor import ArgumentError

            raise ArgumentError(
                "attribute_policy",
                value=attribute_policy,
                caller="molsysmt.native.Structures.append",
            )

        incoming = {
            "structure_id": structure_id,
            "time": _raw_value(time, "ps"),
            "coordinates": _raw_value(coordinates, "nm"),
            "velocities": _raw_value(velocities, "nm/ps"),
            "box": _raw_value(box, "nm"),
            "b_factor": _raw_value(b_factor, "nm**2"),
            "alternate_location": alternate_location,
            "occupancy": occupancy,
            "temperature": _raw_value(temperature, "K"),
            "potential_energy": _raw_value(potential_energy, "kJ/mol"),
            "kinetic_energy": _raw_value(kinetic_energy, "kJ/mol"),
        }

        if not is_all(structure_indices):
            for name, value in incoming.items():
                if value is not None:
                    incoming[name] = np.asarray(value)[structure_indices]
        if not is_all(atom_indices):
            for name in _ATOM_ALIGNED_ATTRIBUTES:
                value = incoming[name]
                if value is not None:
                    incoming[name] = np.asarray(value)[:, atom_indices, ...]

        current = self._frame_payload()
        current_n_structures, current_n_atoms = self._payload_dimensions(
            current,
            caller="molsysmt.native.Structures.append",
        )
        incoming_n_structures, incoming_n_atoms = self._payload_dimensions(
            incoming,
            caller="molsysmt.native.Structures.append",
            payload_error=True,
        )

        if incoming_n_structures == 0:
            return

        if current_n_atoms and incoming_n_atoms and current_n_atoms != incoming_n_atoms:
            raise ArgumentLengthError(
                argument="coordinates (atoms)",
                expected=current_n_atoms,
                actual=incoming_n_atoms,
                caller="molsysmt.native.Structures.append",
            )

        current_present = {name for name, value in current.items() if value is not None}
        incoming_present = {
            name for name, value in incoming.items() if value is not None
        }

        if current_n_structures == 0:
            candidate = incoming
            dropped = []
        else:
            common = current_present & incoming_present
            if not common:
                raise StructuralInconsistencyError(
                    reason=(
                        "Non-empty structural blocks share no frame-aligned "
                        "attribute and cannot be concatenated."
                    ),
                    caller="molsysmt.native.Structures.append",
                )
            dropped = [
                name
                for name in _FRAME_ATTRIBUTES
                if name in current_present ^ incoming_present
            ]
            if dropped and attribute_policy == "strict":
                raise StructuralInconsistencyError(
                    reason=(
                        "One-sided structural attributes are not allowed by "
                        f"strict policy: {', '.join(dropped)}."
                    ),
                    caller="molsysmt.native.Structures.append",
                )

            candidate = {}
            for name in _FRAME_ATTRIBUTES:
                if name not in common:
                    candidate[name] = None
                    continue
                left = current[name]
                right = incoming[name]
                if name == "alternate_location":
                    candidate[name] = list(left) + list(right)
                else:
                    candidate[name] = np.concatenate((left, right), axis=0)

        self._payload_dimensions(
            candidate,
            caller="molsysmt.native.Structures.append",
        )
        if dropped:
            from molsysmt._private.smonitor import StructuralAttributeDropWarning

            warn(
                StructuralAttributeDropWarning(attributes=dropped),
                stacklevel=2,
            )
        self._assign_frame_payload(candidate)

        return

    @signal(tags=["native"])
    @arg_digest(form="molsysmt.Structures")
    def append_structures(
        self,
        item,
        structure_indices="all",
        attribute_policy="intersection",
        skip_digestion=False,
    ):

        return self.append(
            structure_id=item.structure_id,
            time=item.time,
            coordinates=item.coordinates,
            velocities=item.velocities,
            box=item.box,
            temperature=item.temperature,
            potential_energy=item.potential_energy,
            kinetic_energy=item.kinetic_energy,
            b_factor=item.b_factor,
            alternate_location=item.alternate_location,
            occupancy=item.occupancy,
            atom_indices="all",
            structure_indices=structure_indices,
            attribute_policy=attribute_policy,
            skip_digestion=True,
        )

    def _puw_concatenate(self, items, axis=0):
        vals = []
        for ii in items:
            if ii is not None:
                if puw.is_quantity(ii):
                    vals.append(puw.get_value(ii))
                else:
                    vals.append(ii)
        if len(vals) == 0:
            return None
        val = np.concatenate(vals, axis=axis)
        if puw.is_quantity(items[0]):
            return puw.quantity(val, puw.get_unit(items[0]))
        return val

    @arg_digest()
    def _append_structure_id(
        self, structure_id, structure_indices="all", skip_digestion=False
    ):
        if self.structure_id is None:
            if is_all(structure_indices):
                self.structure_id = structure_id
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self.structure_id = np.concatenate([self.structure_id, structure_id])
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_time(self, time, structure_indices="all", skip_digestion=False):
        if self._time is None:
            if is_all(structure_indices):
                self._time = time
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._time = self._puw_concatenate([self._time, time], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_coordinates(
        self,
        coordinates,
        atom_indices="all",
        structure_indices="all",
        skip_digestion=False,
    ):
        if self._coordinates is None:
            if is_all(atom_indices) and is_all(structure_indices):
                self.coordinates = coordinates
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(atom_indices) and is_all(structure_indices):
                coords_raw = _raw_value(coordinates, "nm")
                new_coords = np.concatenate([self._coordinates, coords_raw], axis=0)
                self.coordinates = new_coords
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_velocities(
        self,
        velocities,
        atom_indices="all",
        structure_indices="all",
        skip_digestion=False,
    ):
        if self._velocities is None:
            if is_all(atom_indices) and is_all(structure_indices):
                self._velocities = velocities
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(atom_indices) and is_all(structure_indices):
                self._velocities = self._puw_concatenate(
                    [self._velocities, velocities], axis=0
                )
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_box(self, box, structure_indices="all", skip_digestion=False):
        if self._box is None:
            if is_all(structure_indices):
                self.box = box
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                box_raw = _raw_value(box, "nm")
                new_box = np.concatenate([self._box, box_raw], axis=0)
                self.box = new_box
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_temperature(
        self, temperature, structure_indices="all", skip_digestion=False
    ):
        if self._temperature is None:
            if is_all(structure_indices):
                self._temperature = temperature
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._temperature = self._puw_concatenate(
                    [self._temperature, temperature], axis=0
                )
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_potential_energy(
        self, potential_energy, structure_indices="all", skip_digestion=False
    ):
        if self._potential_energy is None:
            if is_all(structure_indices):
                self._potential_energy = potential_energy
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._potential_energy = self._puw_concatenate(
                    [self._potential_energy, potential_energy], axis=0
                )
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_kinetic_energy(
        self, kinetic_energy, structure_indices="all", skip_digestion=False
    ):
        if self._kinetic_energy is None:
            if is_all(structure_indices):
                self._kinetic_energy = kinetic_energy
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._kinetic_energy = self._puw_concatenate(
                    [self._kinetic_energy, kinetic_energy], axis=0
                )
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_b_factor(self, b_factor, structure_indices="all", skip_digestion=False):
        if self._b_factor is None:
            if is_all(structure_indices):
                self._b_factor = b_factor
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._b_factor = self._puw_concatenate(
                    [self._b_factor, b_factor], axis=0
                )
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_alternate_location(
        self, alternate_location, structure_indices="all", skip_digestion=False
    ):
        if self.alternate_location is None:
            if is_all(structure_indices):
                self.alternate_location = alternate_location
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self.alternate_location = np.concatenate(
                    [self.alternate_location, alternate_location]
                )
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_occupancy(
        self, occupancy, structure_indices="all", skip_digestion=False
    ):
        if self._occupancy is None:
            if is_all(structure_indices):
                self._occupancy = occupancy
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._occupancy = np.concatenate([self._occupancy, occupancy])
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def copy(self, deep=True, *, skip_digestion=False):
        """Copying independently editable structures with controlled allocation.

        Parameters
        ----------
        deep : bool, default=True
            Copy coordinate/box bytes eagerly. False shares protected blocks
            until edits replace affected blocks. Other mutable series and
            metadata are copied independently in both modes.
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        Structures
            Independent structure data preserving units, axes and concrete type.

        Notes
        -----
        Python copy.copy uses the deferred allocation mode; copy.deepcopy uses
        eager coordinate/box allocation and the enclosing workflow's memo.
        Full coordinates/box properties may assemble multiple blocks. Selected
        get() and specialized getters read the requested structures directly.
        MolSys.copy also owns its copied topology, chemistry and analysis handles
        independently, with the same eager/deferred geometry allocation choice.
        Standalone copies omit their weak molecular owner, including an owner
        stored in an extension slot. Other slots retain their declaring classes,
        values and shared-memo aliases.

        Examples
        --------
        >>> structures = Structures(coordinates=puw.quantity(np.zeros((2, 3, 3)), 'nm'))
        >>> duplicate = structures.copy(deep=False)
        >>> duplicate.set_coordinates(indices=[0], structure_indices=[1],
        ...     value=puw.quantity([[[1., 2., 3.]]], 'nm'))
        >>> float(puw.get_value(structures.get_coordinates(), to_unit='nm').sum())
        0.0

        .. versionadded:: 1.0.0
        """
        if not isinstance(skip_digestion, bool):
            from molsysmt._private.argdigest.argument.skip_digestion import (
                digest_skip_digestion,
            )

            digest_skip_digestion(skip_digestion)
        return deepcopy(self) if deep else self.__copy__()

    def __copy__(self):
        """Copying domain handles while sharing protected coordinate/box blocks."""
        from ._copy import _clone, _deferred_geometry_memo

        return _clone(
            self, _deferred_geometry_memo(self), exclude=("_molsys_owner_ref",)
        )

    def __deepcopy__(self, memo):
        """Copying eager structure data without running restoration or migration."""
        from ._copy import _clone

        return _clone(self, memo, exclude=("_molsys_owner_ref",))

    @arg_digest()
    def extract(
        self,
        atom_indices="all",
        structure_indices="all",
        copy_if_all=True,
        skip_digestion=False,
    ):
        if is_all(atom_indices) and is_all(structure_indices):
            if copy_if_all:
                return self.copy()
            else:
                return self

        tmp_item = Structures()

        if self.structure_id is not None:
            if is_all(structure_indices):
                tmp_item.structure_id = deepcopy(self.structure_id)
            else:
                tmp_item.structure_id = deepcopy(self.structure_id[structure_indices])

        if self.time is not None:
            if is_all(structure_indices):
                tmp_item.time = deepcopy(self.time)
            else:
                tmp_item.time = deepcopy(self.time[structure_indices])

        if self._coordinates is not None:
            tmp_item.coordinates = self.get_coordinates(
                indices=atom_indices,
                structure_indices=structure_indices,
                skip_digestion=True,
            )

        if self._box is not None:
            tmp_item.box = self.get_box(
                structure_indices=structure_indices, skip_digestion=True
            )

        if self.velocities is not None:
            if is_all(structure_indices):
                if is_all(atom_indices):
                    tmp_item.velocities = deepcopy(self.velocities)
                else:
                    tmp_item.velocities = deepcopy(self.velocities[:, atom_indices, :])
            else:
                if is_all(atom_indices):
                    tmp_item.velocities = deepcopy(
                        self.velocities[structure_indices, :, :]
                    )
                else:
                    tmp_item.velocities = deepcopy(
                        self.velocities[
                            np.ix_(structure_indices, atom_indices, [0, 1, 2])
                        ]
                    )

        if self.b_factor is not None:
            if is_all(structure_indices):
                if is_all(atom_indices):
                    tmp_item.b_factor = deepcopy(self.b_factor)
                else:
                    tmp_item.b_factor = deepcopy(self.b_factor[:, atom_indices])
            else:
                if is_all(atom_indices):
                    tmp_item.b_factor = deepcopy(self.b_factor[structure_indices, :])
                else:
                    tmp_item.b_factor = deepcopy(
                        self.b_factor[np.ix_(structure_indices, atom_indices)]
                    )

        if self.alternate_location is not None:
            if is_all(structure_indices):
                tmp_item.alternate_location = deepcopy(self.alternate_location)
            elif isinstance(self.alternate_location, np.ndarray):
                tmp_item.alternate_location = deepcopy(
                    self.alternate_location[np.asarray(structure_indices)]
                )
            else:
                tmp_item.alternate_location = [
                    deepcopy(self.alternate_location[index])
                    for index in structure_indices
                ]
            tmp_item.alternate_location = _remap_alternate_atom_indices(
                tmp_item.alternate_location, atom_indices
            )

        if self._occupancy is not None:
            if is_all(structure_indices):
                if is_all(atom_indices):
                    tmp_item.occupancy = deepcopy(self._occupancy)
                else:
                    tmp_item.occupancy = deepcopy(self._occupancy[:, atom_indices])
            else:
                if is_all(atom_indices):
                    tmp_item.occupancy = deepcopy(self._occupancy[structure_indices, :])
                else:
                    tmp_item.occupancy = deepcopy(
                        self._occupancy[np.ix_(structure_indices, atom_indices)]
                    )

        if self.bioassembly is not None:
            tmp_item.bioassembly = deepcopy(self.bioassembly)

        if self.temperature is not None:
            if is_all(structure_indices):
                tmp_item.temperature = deepcopy(self.temperature)
            else:
                tmp_item.temperature = deepcopy(self.temperature[structure_indices])

        if self.potential_energy is not None:
            if is_all(structure_indices):
                tmp_item.potential_energy = deepcopy(self.potential_energy)
            else:
                tmp_item.potential_energy = deepcopy(
                    self.potential_energy[structure_indices]
                )

        if self.kinetic_energy is not None:
            if is_all(structure_indices):
                tmp_item.kinetic_energy = deepcopy(self.kinetic_energy)
            else:
                tmp_item.kinetic_energy = deepcopy(
                    self.kinetic_energy[structure_indices]
                )

        return tmp_item

    @arg_digest()
    def add(
        self,
        item,
        atom_indices="all",
        structure_indices="all",
        attribute_policy="intersection",
        n_atoms_added=None,
        skip_digestion=False,
    ):
        """Concatenating atoms while keeping every atom-aligned series coherent.

        `n_atoms_added` lets a caller that also owns the topology — `MolSys.add` — say
        how many atoms the operation really adds. A topology-only source contributes no
        structural array, so the payload alone cannot tell that the system grew.
        """

        from molsysmt._private.smonitor import (
            IncompatibleBoxWarning,
            StructuralAttributeDropWarning,
            StructuralInconsistencyError,
        )

        caller = "molsysmt.native.Structures.add"

        current = self._frame_payload()
        current_n_structures, current_n_atoms = self._payload_dimensions(
            current, caller=caller
        )
        incoming = item.extract(
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            copy_if_all=True,
            skip_digestion=True,
        )._frame_payload()
        incoming_n_structures, incoming_n_atoms = self._payload_dimensions(
            incoming, caller=caller, payload_error=True
        )

        # A source carrying no structural series at all is a topology-only addition. It
        # has no structure axis to disagree about, so comparing counts would report a
        # length mismatch for a series the caller never supplied.
        source_is_structureless = all(value is None for value in incoming.values())
        if (
            not source_is_structureless
            and current_n_structures != incoming_n_structures
        ):
            raise ArgumentLengthError(
                argument="structures",
                expected=current_n_structures,
                actual=incoming_n_structures,
                caller=caller,
            )

        if n_atoms_added is None:
            n_atoms_added = incoming_n_atoms

        candidate = dict(current)
        dropped = []
        one_sided = []
        for name in _ATOM_ALIGNED_ATTRIBUTES:
            left = current.get(name)
            right = incoming.get(name)
            if left is None or right is None:
                candidate[name] = None
                if (left is None) != (right is None):
                    one_sided.append(name)
                continue
            candidate[name] = np.concatenate((left, right), axis=1)

        if one_sided and attribute_policy == "strict":
            raise StructuralInconsistencyError(
                reason=(
                    "These atom-aligned attributes are present on only one side, so the "
                    f"result would cover part of the atom axis: {', '.join(one_sided)}; use "
                    "attribute_policy='intersection' to discard them instead"
                ),
                caller=caller,
            )
        dropped.extend(one_sided)

        box_reason = _box_mismatch_reason(current.get("box"), incoming.get("box"))

        # add() grows the atom axis; it never reinterprets the unit cell, so the target's
        # box stands and the disagreement is reported rather than resolved.
        if n_atoms_added and box_reason is not None:
            warn(
                IncompatibleBoxWarning(reason=box_reason, caller="molsysmt.add"),
                stacklevel=2,
            )

        # temperature and the energies describe the system, and the system just changed.
        # time and structure_id describe the structure axis, which add() does not touch.
        if n_atoms_added:
            for name in _SYSTEM_LEVEL_OBSERVABLES:
                if candidate.get(name) is not None:
                    candidate[name] = None
                    dropped.append(name)

        candidate["alternate_location"] = _merge_alternate_locations(
            current.get("alternate_location"),
            incoming.get("alternate_location"),
            atom_offset=current_n_atoms,
            n_structures=current_n_structures,
        )

        self._payload_dimensions(candidate, caller=caller)
        if dropped:
            warn(
                StructuralAttributeDropWarning(
                    attributes=dropped, caller="molsysmt.add"
                ),
                stacklevel=2,
            )
        self._assign_frame_payload(candidate)
        return

    @arg_digest()
    def get_coordinates(
        self, indices="all", structure_indices="all", skip_digestion=False
    ):
        """Getting owned coordinates for selected atoms and structures.

        Parameters
        ----------
        indices : str or array-like of int, default='all'
            Atom indices, preserving order and repetitions.
        structure_indices : str or array-like of int, default='all'
            Structure indices, preserving order and repetitions.
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        quantity or None
            Editable coordinates in nm with shape (n_structures, n_atoms, 3),
            independent of stored data. None denotes an absent coordinate series.

        Notes
        -----
        Selected reads access pertinent protected blocks. A complete read needs
        its complete output array. Use get(coordinates=True) for session output units.

        .. versionadded:: 1.0.0
        """

        if self._coordinates is None:
            return None
        return puw.quantity(self._coordinates._select(structure_indices, indices), "nm")

    @arg_digest()
    def set_coordinates(
        self, indices="all", structure_indices="all", value=None, skip_digestion=False
    ):
        """Assigning coordinates with independent protected storage.

        Parameters
        ----------
        indices : str or array-like of int, default='all'
            Atom indices to update. Repetitions use the last supplied value.
        structure_indices : str or array-like of int, default='all'
            Structure indices to update. Repetitions use the last supplied value.
        value : quantity, default=None
            Length-valued coordinates with shape (n_selected_structures,
            n_selected_atoms, 3). Stored values use nm. An explicit quantity is
            required; assign coordinates=None to clear the complete series.
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        None
            Coordinates are replaced on this domain.

        Notes
        -----
        Full selections initialize or replace the series. Partial writes to an
        existing series prepare affected blocks before publication; empty axes
        do nothing. When attached to a MolSys, successful edits invalidate all
        named analyses on the affected structures, including evaluated-empty
        coverage. Other structures and previously obtained snapshots survive.
        No detector runs automatically. Copies of this domain have no owner.

        Examples
        --------
        >>> structures = Structures(coordinates=puw.quantity(np.zeros((1, 1, 3)), 'nm'))
        >>> structures.set_coordinates(indices=[0], structure_indices=[0],
        ...     value=puw.quantity([[[10., 20., 30.]]], 'angstrom'))
        >>> np.allclose(puw.get_value(structures.get_coordinates(), to_unit='nm'), [[[1., 2., 3.]]])
        True

        .. versionadded:: 1.0.0
        """
        if is_all(indices) and is_all(structure_indices):
            self.coordinates = value
        elif self._coordinates is not None:
            candidate = self._coordinates._replace(
                _raw_value(value, "nm"), structure_indices, indices
            )
            self._publish_geometry("coordinates", candidate, structure_indices, indices)

    @arg_digest()
    def get_velocities(
        self, indices="all", structure_indices="all", skip_digestion=False
    ):

        if is_all(indices):
            if is_all(structure_indices):
                return self.velocities.copy()
            else:
                return self.velocities[structure_indices, :, :].copy()
        else:
            if is_all(structure_indices):
                return self.velocities[:, indices, :].copy()
            else:
                return self.velocities[
                    np.ix_(structure_indices, indices, [0, 1, 2])
                ].copy()

    @arg_digest()
    def set_velocities(
        self, indices="all", structure_indices="all", value=None, skip_digestion=False
    ):

        if is_all(indices):
            if is_all(structure_indices):
                self.velocities = value
            else:
                self.velocities[structure_indices, :, :] = value[:, :, :]
        else:
            if is_all(structure_indices):
                self.velocities[:, indices, :] = value[:, :, :]
            else:
                self.velocities[np.ix_(structure_indices, indices)] = value[:, :, :]

        pass

    @arg_digest()
    def get_b_factor(
        self, indices="all", structure_indices="all", skip_digestion=False
    ):

        if is_all(indices):
            if is_all(structure_indices):
                return self.b_factor.copy()
            else:
                return self.b_factor[structure_indices, :].copy()
        else:
            if is_all(structure_indices):
                return self.b_factor[:, indices].copy()
            else:
                return self.b_factor[np.ix_(structure_indices, indices)].copy()

        pass

    @arg_digest()
    def set_b_factor(
        self, indices="all", structure_indices="all", value=None, skip_digestion=False
    ):

        if is_all(indices):
            if is_all(structure_indices):
                self.b_factor = value
            else:
                self.b_factor[structure_indices, :] = value[:, :]
        else:
            if is_all(structure_indices):
                self.b_factor[:, indices] = value[:, :]
            else:
                self.b_factor[np.ix_(structure_indices, indices)] = value[:, :]

        pass

    @arg_digest()
    def get_occupancy(
        self, indices="all", structure_indices="all", skip_digestion=False
    ):
        if self._occupancy is None:
            return None
        if is_all(indices):
            if is_all(structure_indices):
                return self._occupancy.copy()
            else:
                return self._occupancy[structure_indices, :].copy()
        else:
            if is_all(structure_indices):
                return self._occupancy[:, indices].copy()
            else:
                return self._occupancy[np.ix_(structure_indices, indices)].copy()

    @arg_digest()
    def set_occupancy(
        self, indices="all", structure_indices="all", value=None, skip_digestion=False
    ):
        if self._occupancy is None:
            n_structures = (
                self.coordinates.shape[0] if self.coordinates is not None else 1
            )
            n_atoms = self.coordinates.shape[1] if self.coordinates is not None else 0
            self._occupancy = np.empty((n_structures, n_atoms), dtype=object)
        if is_all(indices):
            if is_all(structure_indices):
                self._occupancy = value
            else:
                self._occupancy[structure_indices, :] = value[:, :]
        else:
            if is_all(structure_indices):
                self._occupancy[:, indices] = value[:, :]
            else:
                self._occupancy[np.ix_(structure_indices, indices)] = value[:, :]

    @arg_digest()
    def get_structure_id(self, structure_indices="all", skip_digestion=False):

        if is_all(structure_indices):
            return self.structure_id.copy()
        else:
            return self.structure_id[structure_indices].copy()

        pass

    @arg_digest()
    def set_structure_id(
        self, structure_indices="all", value=None, skip_digestion=False
    ):

        if is_all(structure_indices):
            self.structure_id = value
        else:
            self.structure_id[structure_indices] = value

        pass

    @arg_digest()
    def get_time(self, structure_indices="all", skip_digestion=False):

        if is_all(structure_indices):
            return self.time.copy()
        else:
            return self.time[structure_indices].copy()

    @arg_digest()
    def set_time(self, structure_indices="all", value=None, skip_digestion=False):

        if is_all(structure_indices):
            self.time = value
        else:
            self.time[structure_indices] = value

        pass

    @arg_digest()
    def get_box(self, structure_indices="all", skip_digestion=False):
        """Getting owned periodic box vectors for selected structures.

        Parameters
        ----------
        structure_indices : str or array-like of int, default='all'
            Structure indices, preserving order and repetitions.
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        quantity or None
            Editable boxes in nm with shape (n_structures, 3, 3), independent of
            stored data. Box vectors are rows. None denotes an absent box series.

        Notes
        -----
        Selected reads access pertinent protected blocks. Use get(box=True) for
        session output units.

        .. versionadded:: 1.0.0
        """
        if self._box is None:
            return None
        return puw.quantity(self._box._select(structure_indices), "nm")

    @arg_digest()
    def set_box(self, structure_indices="all", value=None, skip_digestion=False):
        """Assigning periodic boxes to all or selected structures.

        Parameters
        ----------
        structure_indices : int, list, tuple, or numpy.ndarray, default='all'
            Structure indices (0-based) to update. Use 'all' to initialize a
            missing box series; a partial update requires an existing series.
        value : quantity, default=None
            Box matrices with shape (n_selected_structures, 3, 3), carrying
            length units. An explicit quantity is required. Internal storage
            uses nm; assign box=None to clear the complete series.
        skip_digestion : bool, default=False
            Whether to skip MolSysMT's internal argument digestion mechanism.

        Returns
        -------
        None
            The object is updated in place.

        Raises
        ------
        StructuralInconsistencyError
            If a partial update is requested before a box series exists.

        Notes
        -----
        When attached to a MolSys, successful box edits or clearing the full
        series invalidate all named analyses on the affected structures.
        Untouched structures and earlier snapshots survive. Invalid writes
        leave geometry and analyses unchanged; no detector runs automatically.

        .. versionadded:: 1.0.0
        """
        if is_all(structure_indices):
            self.box = value
            return
        if self._box is None:
            if np.asarray(structure_indices).size == 0:
                return
            raise StructuralInconsistencyError(
                reason="Initialize the full box series before updating selected structures.",
                caller="molsysmt.native.Structures.set_box",
            )

        candidate = self._box._replace(_raw_value(value, "nm"), structure_indices)
        self._publish_geometry("box", candidate, structure_indices)
