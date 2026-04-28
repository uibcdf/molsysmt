from molsysmt._private.variables import is_all
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import ArgumentLengthError, NotImplementedMethodError
from molsysmt import pyunitwizard as puw
from copy import deepcopy
import numpy as np
from smonitor import signal

class Structures:
    """Storing per-structure data (coordinates, box, time, energies) for a molecular system."""

    @property
    def n_structures(self):
        if self.coordinates is not None:
            return self.coordinates.shape[0]
        elif self.velocities is not None:
            return self.velocities.shape[0]
        elif self.box is not None:
            return self.box.shape[0]
        else:
            return 0

    @property
    def n_atoms(self):
        if self.coordinates is not None:
            return self.coordinates.shape[1]
        elif self.velocities is not None:
            return self.velocities.shape[1]
        else:
            return 0

    @signal(tags=['native'])
    @arg_digest()
    def __init__(self, constant_time_step=False, time_step=None, constant_id_step=False,
            id_step=None, constant_box=False,
            structure_id=None, time=None, coordinates=None, velocities=None, box=None,
            b_factor=None, alternate_location=None, bioassembly=None,
            temperature=None, potential_energy=None, kinetic_energy=None, skip_digestion=False):

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

    @signal(tags=['native'])
    @arg_digest()
    def append(self, structure_id=None, time=None, coordinates=None, velocities=None,
               box=None, temperature=None, potential_energy=None, kinetic_energy=None,
               b_factor=None, alternate_location=None,
               atom_indices='all', structure_indices='all', skip_digestion=False):
        """Append one or more structures and associated metadata to this object."""

        # 1. Validation of internal consistency of the incoming data
        incoming_n_structures = None
        
        if structure_id is not None and len(structure_id) > 0:
            incoming_n_structures = len(structure_id)
            
        if time is not None and len(time) > 0:
            if incoming_n_structures is None:
                incoming_n_structures = len(time)
            elif incoming_n_structures != len(time):
                raise ArgumentLengthError(argument="time", expected=incoming_n_structures, actual=len(time), caller="molsysmt.native.Structures.append")

        if coordinates is not None:
            if incoming_n_structures is None:
                incoming_n_structures = coordinates.shape[0]
            elif incoming_n_structures != coordinates.shape[0]:
                raise ArgumentLengthError(argument="coordinates (frames)", expected=incoming_n_structures, actual=coordinates.shape[0], caller="molsysmt.native.Structures.append")
            
            if self.n_atoms > 0 and self.n_atoms != coordinates.shape[1]:
                 raise ArgumentLengthError(argument="coordinates (atoms)", expected=self.n_atoms, actual=coordinates.shape[1], caller="molsysmt.native.Structures.append")

        if box is not None and len(box) > 0:
            if incoming_n_structures is None:
                incoming_n_structures = box.shape[0]
            elif incoming_n_structures != box.shape[0]:
                raise ArgumentLengthError(argument="box", expected=incoming_n_structures, actual=box.shape[0], caller="molsysmt.native.Structures.append")

        if incoming_n_structures is None:
            return

        # 2. Actual Append
        if structure_id is not None and len(structure_id) > 0:
            self._append_structure_id(structure_id, structure_indices=structure_indices, skip_digestion=True)
        
        if time is not None and len(time) > 0:
            self._append_time(time, structure_indices=structure_indices, skip_digestion=True)

        if coordinates is not None:
            self._append_coordinates(coordinates, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

        if velocities is not None:
            self._append_velocities(velocities, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

        if box is not None and len(box) > 0:
            self._append_box(box, structure_indices=structure_indices, skip_digestion=True)

        if temperature is not None:
            self._append_temperature(temperature, structure_indices=structure_indices, skip_digestion=True)

        if potential_energy is not None:
            self._append_potential_energy(potential_energy, structure_indices=structure_indices, skip_digestion=True)

        if kinetic_energy is not None:
            self._append_kinetic_energy(kinetic_energy, structure_indices=structure_indices, skip_digestion=True)

        if b_factor is not None:
            self._append_b_factor(b_factor, structure_indices=structure_indices, skip_digestion=True)

        if alternate_location is not None:
            self._append_alternate_location(alternate_location, structure_indices=structure_indices, skip_digestion=True)

        return

    @signal(tags=['native'])
    @arg_digest(form='molsysmt.Structures')
    def append_structures(self, item, structure_indices='all', skip_digestion=False):

        return self.append(structure_id=item.structure_id, time=item.time, coordinates=item.coordinates,
                           velocities=item.velocities, box=item.box, temperature=item.temperature,
                           potential_energy=item.potential_energy, kinetic_energy=item.kinetic_energy,
                           b_factor=item.b_factor, alternate_location=item.alternate_location,
                           atom_indices='all', structure_indices=structure_indices, skip_digestion=True)

    def _puw_concatenate(self, items, axis=0):
        val = np.concatenate([puw.get_value(ii) for ii in items if ii is not None], axis=axis)
        unit = puw.get_unit(items[0])
        return puw.quantity(val, unit)

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
        if self.time is None:
            if is_all(structure_indices):
                self.time = time
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self.time = self._puw_concatenate([self.time, time], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_coordinates(self, coordinates, atom_indices='all', structure_indices='all', skip_digestion=False):
        if self.coordinates is None:
            if is_all(atom_indices) and is_all(structure_indices):
                self.coordinates = coordinates
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(atom_indices) and is_all(structure_indices):
                self.coordinates = self._puw_concatenate([self.coordinates, coordinates], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_velocities(self, velocities, atom_indices='all', structure_indices='all', skip_digestion=False):
        if self.velocities is None:
            if is_all(atom_indices) and is_all(structure_indices):
                self.velocities = velocities
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(atom_indices) and is_all(structure_indices):
                self.velocities = self._puw_concatenate([self.velocities, velocities], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_box(self, box, structure_indices='all', skip_digestion=False):
        if self.box is None:
            if is_all(structure_indices):
                self.box = box
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self.box = self._puw_concatenate([self.box, box], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_temperature(self, temperature, structure_indices='all', skip_digestion=False):
        if self.temperature is None:
            if is_all(structure_indices):
                self.temperature = temperature
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self.temperature = self._puw_concatenate([self.temperature, temperature], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_potential_energy(self, potential_energy, structure_indices='all', skip_digestion=False):
        if self.potential_energy is None:
            if is_all(structure_indices):
                self.potential_energy = potential_energy
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self.potential_energy = self._puw_concatenate([self.potential_energy, potential_energy], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_kinetic_energy(self, kinetic_energy, structure_indices='all', skip_digestion=False):
        if self.kinetic_energy is None:
            if is_all(structure_indices):
                self.kinetic_energy = kinetic_energy
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self.kinetic_energy = self._puw_concatenate([self.kinetic_energy, kinetic_energy], axis=0)
            else:
                raise NotImplementedMethodError()

    @arg_digest()
    def _append_b_factor(self, b_factor, structure_indices='all', skip_digestion=False):
        if self.b_factor is None:
            if is_all(structure_indices):
                self.b_factor = b_factor
            else:
                raise NotImplementedMethodError()
        else:
            if is_all(structure_indices):
                self.b_factor = self._puw_concatenate([self.b_factor, b_factor], axis=0)
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
            else:
                tmp_item.alternate_location = deepcopy(self.alternate_location[structure_indices])

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
    
        if is_all(indices):
            if is_all(structure_indices):
    
                self.coordinates = value
    
                if self.box is not None and self.box.shape[0] > 0:
                    if self.box.shape[0]!=self.n_structures:
                        if self.box.shape[0]==1:
                            from molsysmt import pyunitwizard as puw
                            self.box = puw.utils.numpy.repeat(self.box, self.n_structures, axis=0)
                        else:
                            # If we can't broadcast, we set it to None or keep it as is?
                            # For 1.0.0 stability, if it doesn't match and isn't 1, we invalidate the box.
                            self.box = None
            else:
                self.coordinates[structure_indices,:,:] = value[:,:,:]
        else:
            if is_all(structure_indices):
                self.coordinates[:,indices,:] = value[:,:,:]
            else:
                self.coordinates[np.ix_(structure_indices, indices)]=value[:,:,:]
    
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
    
        if is_all(structure_indices):
            self.box = value
        else:
            self.box[structure_indices,:,:] = value[:,:,:]
    
        pass

