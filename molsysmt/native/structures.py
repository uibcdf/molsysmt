from molsysmt._private.variables import is_all
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import (
    ArgumentLengthError,
    NotImplementedMethodError,
    StructuralInconsistencyError,
)
from molsysmt import pyunitwizard as puw
from copy import deepcopy
import numpy as np
from smonitor import signal

def _raw_value(quantity, canonical_unit):
    if quantity is None:
        return None
    if puw.is_quantity(quantity):
        return puw.get_value(quantity, to_unit=canonical_unit)
    return quantity


_FRAME_ATTRIBUTES = (
    'structure_id',
    'time',
    'coordinates',
    'velocities',
    'box',
    'b_factor',
    'alternate_location',
    'occupancy',
    'temperature',
    'potential_energy',
    'kinetic_energy',
)

_ATOM_ALIGNED_ATTRIBUTES = (
    'coordinates',
    'velocities',
    'b_factor',
    'occupancy',
)


class Structures:
    """Storing per-structure data (coordinates, box, time, energies) for a molecular system."""

    @property
    def time_step(self):
        if self._time_step is None:
            return None
        return puw.quantity(self._time_step, 'ps')

    @time_step.setter
    def time_step(self, value):
        self._time_step = _raw_value(value, 'ps')

    @property
    def time(self):
        if self._time is None:
            return None
        return puw.quantity(self._time, 'ps')

    @time.setter
    def time(self, value):
        self._time = _raw_value(value, 'ps')

    @property
    def coordinates(self):
        if self._coordinates is None:
            return None
        # Return a view wrapped in quantity. The view inherits writeable = False.
        return puw.quantity(self._coordinates, 'nm')

    @coordinates.setter
    def coordinates(self, value):
        val = _raw_value(value, 'nm')
        if val is not None:
            val = np.asarray(val, dtype=np.float64)
            # Make the array read-only to prevent side-effects in views
            val.flags.writeable = False
        self._coordinates = val

    @property
    def velocities(self):
        if self._velocities is None:
            return None
        return puw.quantity(self._velocities, 'nm/ps')

    @velocities.setter
    def velocities(self, value):
        self._velocities = _raw_value(value, 'nm/ps')

    @property
    def box(self):
        if self._box is None:
            return None
        return puw.quantity(self._box, 'nm')

    @box.setter
    def box(self, value):
        val = _raw_value(value, 'nm')
        if val is not None:
            val = np.asarray(val, dtype=np.float64)
            # Make the array read-only to prevent side-effects in views
            val.flags.writeable = False
        self._box = val

    @property
    def b_factor(self):
        if self._b_factor is None:
            return None
        return puw.quantity(self._b_factor, 'nm**2')

    @b_factor.setter
    def b_factor(self, value):
        self._b_factor = _raw_value(value, 'nm**2')

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
        return puw.quantity(self._temperature, 'K')

    @temperature.setter
    def temperature(self, value):
        self._temperature = _raw_value(value, 'K')

    @property
    def potential_energy(self):
        if self._potential_energy is None:
            return None
        return puw.quantity(self._potential_energy, 'kJ/mol')

    @potential_energy.setter
    def potential_energy(self, value):
        self._potential_energy = _raw_value(value, 'kJ/mol')

    @property
    def kinetic_energy(self):
        if self._kinetic_energy is None:
            return None
        return puw.quantity(self._kinetic_energy, 'kJ/mol')

    @kinetic_energy.setter
    def kinetic_energy(self, value):
        self._kinetic_energy = _raw_value(value, 'kJ/mol')

    @property
    def n_structures(self):
        n_structures, _ = self._validate_alignment()
        return n_structures

    @property
    def n_atoms(self):
        _, n_atoms = self._validate_alignment()
        return n_atoms

    @signal(tags=['native'])
    @arg_digest()
    def __init__(self, constant_time_step=False, time_step=None, constant_id_step=False,
            id_step=None, constant_box=False,
            structure_id=None, time=None, coordinates=None, velocities=None, box=None,
            b_factor=None, alternate_location=None, bioassembly=None,
            temperature=None, potential_energy=None, kinetic_energy=None,
            occupancy=None, skip_digestion=False):

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
            'structure_id': self.structure_id,
            'time': self._time,
            'coordinates': self._coordinates,
            'velocities': self._velocities,
            'box': self._box,
            'b_factor': self._b_factor,
            'alternate_location': self.alternate_location,
            'occupancy': self._occupancy,
            'temperature': self._temperature,
            'potential_energy': self._potential_energy,
            'kinetic_energy': self._kinetic_energy,
        }

    @staticmethod
    def _payload_dimensions(payload, caller, payload_error=False):
        """Validating shared structure and atom axes for one payload."""

        lengths = {
            name: len(value)
            for name, value in payload.items()
            if value is not None
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
            array = np.asarray(value)
            if array.ndim < 2:
                raise StructuralInconsistencyError(
                    reason=f"Structural attribute {name!r} has no atom axis.",
                    caller=caller,
                )
            atom_sizes[name] = array.shape[1]

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
            caller='molsysmt.native.Structures',
        )

    def _assign_frame_payload(self, payload):
        """Replacing all frame-aligned data from a validated raw payload."""

        for name in _FRAME_ATTRIBUTES:
            setattr(self, name, deepcopy(payload.get(name)))
        self._validate_alignment()

    def __setstate__(self, state):
        """Restore current storage or migrate legacy public array fields."""

        restored = type(self)(skip_digestion=True)
        self.__dict__.update(restored.__dict__)
        if '_coordinates' in state:
            self.__dict__.update(state)
            return

        legacy_fields = {
            'time', 'coordinates', 'velocities', 'box', 'b_factor', 'occupancy',
            'temperature', 'potential_energy', 'kinetic_energy',
        }
        for field in legacy_fields:
            if field in state:
                setattr(self, field, state[field])
        for key, value in state.items():
            if key not in legacy_fields and key not in {'n_atoms', 'n_structures'}:
                self.__dict__[key] = value

    @signal(tags=['native'])
    @arg_digest()
    def append(self, structure_id=None, time=None, coordinates=None, velocities=None,
               box=None, temperature=None, potential_energy=None, kinetic_energy=None,
               b_factor=None, alternate_location=None, occupancy=None,
               atom_indices='all', structure_indices='all',
               attribute_policy='intersection', skip_digestion=False):
        """Append one or more structures and associated metadata to this object."""

        if attribute_policy not in {'intersection', 'strict'}:
            from molsysmt._private.smonitor import ArgumentError

            raise ArgumentError(
                'attribute_policy',
                value=attribute_policy,
                caller='molsysmt.native.Structures.append',
            )

        incoming = {
            'structure_id': structure_id,
            'time': _raw_value(time, 'ps'),
            'coordinates': _raw_value(coordinates, 'nm'),
            'velocities': _raw_value(velocities, 'nm/ps'),
            'box': _raw_value(box, 'nm'),
            'b_factor': _raw_value(b_factor, 'nm**2'),
            'alternate_location': alternate_location,
            'occupancy': occupancy,
            'temperature': _raw_value(temperature, 'K'),
            'potential_energy': _raw_value(potential_energy, 'kJ/mol'),
            'kinetic_energy': _raw_value(kinetic_energy, 'kJ/mol'),
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
            caller='molsysmt.native.Structures.append',
        )
        incoming_n_structures, incoming_n_atoms = self._payload_dimensions(
            incoming,
            caller='molsysmt.native.Structures.append',
            payload_error=True,
        )

        if incoming_n_structures == 0:
            return

        if (
            current_n_atoms
            and incoming_n_atoms
            and current_n_atoms != incoming_n_atoms
        ):
            raise ArgumentLengthError(
                argument='coordinates (atoms)',
                expected=current_n_atoms,
                actual=incoming_n_atoms,
                caller='molsysmt.native.Structures.append',
            )

        current_present = {
            name for name, value in current.items() if value is not None
        }
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
                        'Non-empty structural blocks share no frame-aligned '
                        'attribute and cannot be concatenated.'
                    ),
                    caller='molsysmt.native.Structures.append',
                )
            dropped = [
                name
                for name in _FRAME_ATTRIBUTES
                if name in current_present ^ incoming_present
            ]
            if dropped and attribute_policy == 'strict':
                raise StructuralInconsistencyError(
                    reason=(
                        'One-sided structural attributes are not allowed by '
                        f"strict policy: {', '.join(dropped)}."
                    ),
                    caller='molsysmt.native.Structures.append',
                )

            candidate = {}
            for name in _FRAME_ATTRIBUTES:
                if name not in common:
                    candidate[name] = None
                    continue
                left = current[name]
                right = incoming[name]
                if name == 'alternate_location':
                    candidate[name] = list(left) + list(right)
                else:
                    candidate[name] = np.concatenate((left, right), axis=0)

        self._payload_dimensions(
            candidate,
            caller='molsysmt.native.Structures.append',
        )
        if dropped:
            import warnings
            from molsysmt._private.smonitor import StructuralAttributeDropWarning

            warnings.warn(
                StructuralAttributeDropWarning(attributes=dropped),
                stacklevel=2,
            )
        self._assign_frame_payload(candidate)

        return

    @signal(tags=['native'])
    @arg_digest(form='molsysmt.Structures')
    def append_structures(
        self,
        item,
        structure_indices='all',
        attribute_policy='intersection',
        skip_digestion=False,
    ):

        return self.append(structure_id=item.structure_id, time=item.time, coordinates=item.coordinates,
                           velocities=item.velocities, box=item.box, temperature=item.temperature,
                           potential_energy=item.potential_energy, kinetic_energy=item.kinetic_energy,
                           b_factor=item.b_factor, alternate_location=item.alternate_location,
                           occupancy=item.occupancy,
                           atom_indices='all', structure_indices=structure_indices,
                           attribute_policy=attribute_policy, skip_digestion=True)

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
    def _append_structure_id(self, structure_id, structure_indices='all', skip_digestion=False):
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
    def _append_time(self, time, structure_indices='all', skip_digestion=False):
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
    def _append_coordinates(self, coordinates, atom_indices='all', structure_indices='all', skip_digestion=False):
        if self._coordinates is None:
            if is_all(atom_indices) and is_all(structure_indices):
                self.coordinates = coordinates
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(atom_indices) and is_all(structure_indices):
                coords_raw = _raw_value(coordinates, 'nm')
                new_coords = np.concatenate([self._coordinates, coords_raw], axis=0)
                new_coords.flags.writeable = False
                self._coordinates = new_coords
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_velocities(self, velocities, atom_indices='all', structure_indices='all', skip_digestion=False):
        if self._velocities is None:
            if is_all(atom_indices) and is_all(structure_indices):
                self._velocities = velocities
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(atom_indices) and is_all(structure_indices):
                self._velocities = self._puw_concatenate([self._velocities, velocities], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_box(self, box, structure_indices='all', skip_digestion=False):
        if self._box is None:
            if is_all(structure_indices):
                self.box = box
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                box_raw = _raw_value(box, 'nm')
                new_box = np.concatenate([self._box, box_raw], axis=0)
                new_box.flags.writeable = False
                self._box = new_box
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_temperature(self, temperature, structure_indices='all', skip_digestion=False):
        if self._temperature is None:
            if is_all(structure_indices):
                self._temperature = temperature
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._temperature = self._puw_concatenate([self._temperature, temperature], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_potential_energy(self, potential_energy, structure_indices='all', skip_digestion=False):
        if self._potential_energy is None:
            if is_all(structure_indices):
                self._potential_energy = potential_energy
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._potential_energy = self._puw_concatenate([self._potential_energy, potential_energy], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_kinetic_energy(self, kinetic_energy, structure_indices='all', skip_digestion=False):
        if self._kinetic_energy is None:
            if is_all(structure_indices):
                self._kinetic_energy = kinetic_energy
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._kinetic_energy = self._puw_concatenate([self._kinetic_energy, kinetic_energy], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_b_factor(self, b_factor, structure_indices='all', skip_digestion=False):
        if self._b_factor is None:
            if is_all(structure_indices):
                self._b_factor = b_factor
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self._b_factor = self._puw_concatenate([self._b_factor, b_factor], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_alternate_location(self, alternate_location, structure_indices='all', skip_digestion=False):
        if self.alternate_location is None:
            if is_all(structure_indices):
                self.alternate_location = alternate_location
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self.alternate_location = np.concatenate([self.alternate_location, alternate_location])
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_occupancy(self, occupancy, structure_indices='all', skip_digestion=False):
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

    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

    @arg_digest()
    def extract(self, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
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
                
        if self.coordinates is not None:
            if is_all(structure_indices):
                if is_all(atom_indices):
                    tmp_item.coordinates = deepcopy(self.coordinates)
                else:
                    tmp_item.coordinates = deepcopy(self.coordinates[:, atom_indices, :])
            else:
                if is_all(atom_indices):
                    tmp_item.coordinates = deepcopy(self.coordinates[structure_indices, :, :])
                else:
                    tmp_item.coordinates = deepcopy(self.coordinates[np.ix_(structure_indices, atom_indices, [0,1,2])])

        if self.box is not None:
            if is_all(structure_indices):
                tmp_item.box = deepcopy(self.box)
            else:
                tmp_item.box = deepcopy(self.box[structure_indices, :, :])

        if self.velocities is not None:
            if is_all(structure_indices):
                if is_all(atom_indices):
                    tmp_item.velocities = deepcopy(self.velocities)
                else:
                    tmp_item.velocities = deepcopy(self.velocities[:, atom_indices, :])
            else:
                if is_all(atom_indices):
                    tmp_item.velocities = deepcopy(self.velocities[structure_indices, :, :])
                else:
                    tmp_item.velocities = deepcopy(self.velocities[np.ix_(structure_indices, atom_indices, [0, 1, 2])])

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
                    tmp_item.b_factor = deepcopy(self.b_factor[np.ix_(structure_indices, atom_indices)])

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
            if not is_all(atom_indices):
                atom_index_map = {
                    int(old_index): new_index
                    for new_index, old_index in enumerate(atom_indices)
                }
                remapped = []
                for structure_alternates in tmp_item.alternate_location:
                    if isinstance(structure_alternates, dict):
                        remapped.append({
                            atom_index_map[int(old_index)]: value
                            for old_index, value in structure_alternates.items()
                            if int(old_index) in atom_index_map
                        })
                    else:
                        remapped.append(deepcopy(structure_alternates))
                if isinstance(tmp_item.alternate_location, np.ndarray):
                    remapped = np.asarray(
                        remapped,
                        dtype=tmp_item.alternate_location.dtype,
                    )
                tmp_item.alternate_location = remapped

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
                    tmp_item.occupancy = deepcopy(self._occupancy[np.ix_(structure_indices, atom_indices)])

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
                tmp_item.potential_energy = deepcopy(self.potential_energy[structure_indices])

        if self.kinetic_energy is not None:
            if is_all(structure_indices):
                tmp_item.kinetic_energy = deepcopy(self.kinetic_energy)
            else:
                tmp_item.kinetic_energy = deepcopy(self.kinetic_energy[structure_indices])

        return tmp_item

    @arg_digest()
    def add(self, item, atom_indices='all', structure_indices='all', skip_digestion=False):
        # Concatenate atoms to the current structures
        if is_all(structure_indices):
            if self.n_structures != item.n_structures:
                 raise ArgumentLengthError(argument="structures", expected=self.n_structures, actual=item.n_structures, caller="molsysmt.native.Structures.add")
        
        if item.coordinates is not None:
            if self.coordinates is None:
                 # This is tricky, if coordinates are None we shouldn't be adding atoms
                 from molsysmt._private.smonitor import StructuralInconsistencyError
                 raise StructuralInconsistencyError("Cannot add atom coordinates to a system without coordinates.")
            else:
                 if is_all(structure_indices):
                     if is_all(atom_indices):
                         self.coordinates = self._puw_concatenate([self.coordinates, item.coordinates], axis=1)
                     else:
                         self.coordinates = self._puw_concatenate([self.coordinates, item.coordinates[:, atom_indices, :]], axis=1)
        return

    @arg_digest()
    def get_coordinates(self, indices='all', structure_indices='all', skip_digestion=False):
    
        if is_all(indices):
            if is_all(structure_indices):
                return self.coordinates.copy()
            else:
                return self.coordinates[structure_indices,:,:].copy()
        else:
            if is_all(structure_indices):
                return self.coordinates[:,indices,:].copy()
            else:
                return self.coordinates[np.ix_(structure_indices, indices, [0,1,2])].copy()

    @arg_digest()
    def set_coordinates(self, indices='all', structure_indices='all', value=None, skip_digestion=False):
        if self._coordinates is None:
            return

        self._coordinates.flags.writeable = True
        try:
            raw_val = _raw_value(value, 'nm')
            if is_all(indices):
                if is_all(structure_indices):
                    self._coordinates.flags.writeable = False
                    self.coordinates = value
                    return
                else:
                    self._coordinates[structure_indices,:,:] = raw_val[:,:,:]
            else:
                if is_all(structure_indices):
                    self._coordinates[:,indices,:] = raw_val[:,:,:]
                else:
                    self._coordinates[np.ix_(structure_indices, indices)] = raw_val[:,:,:]
        finally:
            if self._coordinates is not None:
                self._coordinates.flags.writeable = False
    
        pass

    @arg_digest()
    def get_velocities(self, indices='all', structure_indices='all', skip_digestion=False):
    
        if is_all(indices):
            if is_all(structure_indices):
                return self.velocities.copy()
            else:
                return self.velocities[structure_indices,:,:].copy()
        else:
            if is_all(structure_indices):
                return self.velocities[:,indices,:].copy()
            else:
                return self.velocities[np.ix_(structure_indices, indices, [0,1,2])].copy()


    @arg_digest()
    def set_velocities(self, indices='all', structure_indices='all', value=None, skip_digestion=False):
    
        if is_all(indices):
            if is_all(structure_indices):
                self.velocities = value
            else:
                self.velocities[structure_indices,:,:] = value[:,:,:]
        else:
            if is_all(structure_indices):
                self.velocities[:,indices,:] = value[:,:,:]
            else:
                self.velocities[np.ix_(structure_indices, indices)]=value[:,:,:]
    
        pass


    @arg_digest()
    def get_b_factor(self, indices='all', structure_indices='all', skip_digestion=False):
    
        if is_all(indices):
            if is_all(structure_indices):
                return self.b_factor.copy()
            else:
                return self.b_factor[structure_indices,:].copy()
        else:
            if is_all(structure_indices):
                return self.b_factor[:,indices].copy()
            else:
                return self.b_factor[np.ix_(structure_indices, indices)].copy()
    
        pass


    @arg_digest()
    def set_b_factor(self, indices='all', structure_indices='all', value=None, skip_digestion=False):
    
        if is_all(indices):
            if is_all(structure_indices):
                self.b_factor = value
            else:
                self.b_factor[structure_indices,:] = value[:,:]
        else:
            if is_all(structure_indices):
                self.b_factor[:,indices] = value[:,:]
            else:
                self.b_factor[np.ix_(structure_indices, indices)]=value[:,:]
    
        pass


    @arg_digest()
    def get_occupancy(self, indices='all', structure_indices='all', skip_digestion=False):
        if self._occupancy is None:
            return None
        if is_all(indices):
            if is_all(structure_indices):
                return self._occupancy.copy()
            else:
                return self._occupancy[structure_indices,:].copy()
        else:
            if is_all(structure_indices):
                return self._occupancy[:,indices].copy()
            else:
                return self._occupancy[np.ix_(structure_indices, indices)].copy()


    @arg_digest()
    def set_occupancy(self, indices='all', structure_indices='all', value=None, skip_digestion=False):
        if self._occupancy is None:
            n_structures = self.coordinates.shape[0] if self.coordinates is not None else 1
            n_atoms = self.coordinates.shape[1] if self.coordinates is not None else 0
            self._occupancy = np.empty((n_structures, n_atoms), dtype=object)
        if is_all(indices):
            if is_all(structure_indices):
                self._occupancy = value
            else:
                self._occupancy[structure_indices,:] = value[:,:]
        else:
            if is_all(structure_indices):
                self._occupancy[:,indices] = value[:,:]
            else:
                self._occupancy[np.ix_(structure_indices, indices)]=value[:,:]


    @arg_digest()
    def get_structure_id(self, structure_indices='all', skip_digestion=False):
    
        if is_all(structure_indices):
            return self.structure_id.copy()
        else:
            return self.structure_id[structure_indices].copy()
    
        pass


    @arg_digest()
    def set_structure_id(self, structure_indices='all', value=None, skip_digestion=False):
    
        if is_all(structure_indices):
            self.structure_id = value
        else:
            self.structure_id[structure_indices] = value
    
        pass
    

    @arg_digest()
    def get_time(self, structure_indices='all', skip_digestion=False):
    
        if is_all(structure_indices):
            return self.time.copy()
        else:
            return self.time[structure_indices].copy()


    @arg_digest()
    def set_time(self, structure_indices='all', value=None, skip_digestion=False):
    
        if is_all(structure_indices):
            self.time = value
        else:
            self.time[structure_indices] = value
    
        pass
   

    @arg_digest()
    def get_box(self, structure_indices='all', skip_digestion=False):
    
        if is_all(structure_indices):
            return self.box.copy()
        else:
            return self.box[structure_indices,:,:].copy()
    
        pass


    @arg_digest()
    def set_box(self, structure_indices='all', value=None, skip_digestion=False):
        if self._box is None:
            return

        self._box.flags.writeable = True
        try:
            raw_val = _raw_value(value, 'nm')
            if is_all(structure_indices):
                self._box.flags.writeable = False
                self.box = value
            else:
                self._box[structure_indices,:,:] = raw_val[:,:,:]
        finally:
            if self._box is not None:
                self._box.flags.writeable = False
    
        pass
