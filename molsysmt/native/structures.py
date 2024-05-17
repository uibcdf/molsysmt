from copy import deepcopy
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from molsysmt.basic import get
from molsysmt._private.exceptions import IteratorError
from molsysmt._private.digestion import digest

class Structures:
    """ Class to store the trajectory data of a molecular system


        Attributes
        ----------
        box : pint.Quantity of shape (n_structures, 3, 3)
            The box of the molecular system in nanometers.

        coordinates : pint.Quantity of shape (n_structures, n_atoms, 3)
            The coordinates of the trajectory for each frame.

        velocities : pint.Quantity of shape (n_structures, n_atoms, 3)
            The velocities of the trajectory for each frame.

        n_atoms : int
            Number of atoms in the trajectory.

        n_structures : int
            Number of structures or frames in the trajectory.

        time :  pint.Quantity of shape (n_structures, )
            The times of the trajectory in picoseconds.

        id :


    """

    @digest()
    def __init__(self, constant_time_step=False, time_step=None, constant_id_step=False,
            id_step=None, constant_box=False,
            structure_id=None, time=None, coordinates=None, velocities=None, box=None,
            b_factor=None, alternate_location=None, bioassembly=None,
            temperature=None, potential_energy=None, kinetic_energy=None, skip_digestion=False):

        self.n_atoms = 0
        self.n_structures = 0

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

        if coordinates is not None:
            self.n_structures = coordinates.shape[0]
            self.n_atoms = coordinates.shape[1]
        elif velocities is not None:
            self.n_structures = velocities.shape[0]
            self.n_atoms = velocities.shape[1]
        elif box is not None:
            self.n_structures = box.shape[0]
        else:
            self.n_structures = 0
            self.n_atoms = 0


    @digest()
    def _append_structure_id(self, structure_id, structure_indices='all', skip_digestion=False):

        if self.structure_id is None:
            if is_all(structure_indices):
                self.structure_id = deepcopy(structure_id)
            else:
                self.structure_id = structure_id[structure_indices]
        else:
            if is_all(structure_indices):
                self.structure_id = np.concatenate([self.structure_id, structure_id])
            else:
                self.structure_id = np.concatenate([self.structure_id, structure_id[structure_indices]])


    @digest()
    def _append_time(self, time, structure_indices='all', skip_digestion=False):

        time = puw.standardize(time)

        if self.time is None:
            if is_all(structure_indices):
                self.time = deepcopy(time)
            else:
                self.time = time[structure_indices]
        else:
            if is_all(structure_indices):
                self.time = np.concatenate([self.time, time])
            else:
                self.time = np.concatenate([self.time, time[structure_indices]])


    @digest()
    def _append_coordinates(self, coordinates, atom_indices='all', structure_indices='all', skip_digestion=False):

        coordinates = puw.standardize(coordinates)

        if self.coordinates is None:
            if is_all(structure_indices):
                if is_all(atom_indices):
                    self.coordinates = deepcopy(coordinates)
                else:
                    self.coordinates = coordinates[:,atom_indices,:]
            else:
                if is_all(atom_indices):
                    self.coordinates = coordinates[structure_indices,:,:]
                else:
                    self.coordinates = coordinates[np.ix_(structure_indices, atom_indices)]
        else:
            if self.coordinates.shape[1] != coordinates.shape[1]:
                raise ValueError(
                    "The coordinates to be appended in the system "
                    "need to have the same number of atoms.")

            if is_all(structure_indices):
                if is_all(atom_indices):
                    self.coordinates = np.concatenate([self.coordinates, coordinates])
                else:
                    self.coordinates = np.concatenate([self.coordinates, coordinates[:,atom_indices,:]])
            else:
                if is_all(atom_indices):
                    self.coordinates = np.concatenate([self.coordinates, coordinates[structure_indices,:,:]])
                else:
                    self.coordinates = np.concatenate([self.coordinates,
                                                       coordinates[np.ix_(structure_indices, atom_indices)]])

    @digest()
    def _append_velocities(self, velocities, atom_indices='all', structure_indices='all', skip_digestion=False):

        velocities = puw.standardize(velocities)

        if self.velocities is None:
            if is_all(structure_indices):
                if is_all(atom_indices):
                    self.velocities = deepcopy(velocities)
                else:
                    self.velocities = velocities[:,atom_indices,:]
            else:
                if is_all(atom_indices):
                    self.velocities = velocities[structure_indices,:,:]
                else:
                    self.velocities = velocities[np.ix_(structure_indices, atom_indices)]
        else:
            if self.velocities.shape[1] != velocities.shape[1]:
                raise ValueError(
                    "The velocities to be appended in the system "
                    "need to have the same number of atoms.")
            if is_all(structure_indices):
                if is_all(atom_indices):
                    self.velocities = np.concatenate([self.velocities, velocities])
                else:
                    self.velocities = np.concatenate([self.velocities, velocities[:,atom_indices,:]])
            else:
                if is_all(atom_indices):
                    self.velocities = np.concatenate([self.velocities, velocities[structure_indices,:,:]])
                else:
                    self.velocities = np.concatenate([self.velocities,
                                                       velocities[np.ix_(structure_indices, atom_indices)]])


    @digest()
    def _append_box(self, box, structure_indices='all', skip_digestion=False):

        box = puw.standardize(box)

        if self.box is None:
            if is_all(structure_indices):
                self.box = deepcopy(box)
            else:
                self.box = box[structure_indices]
        else:
            if is_all(structure_indices):
                self.box = np.concatenate([self.box, box])
            else:
                self.box = np.concatenate([self.box, box[structure_indices]])


    @digest()
    def _append_temperature(self, temperature, structure_indices='all', skip_digestion=False):

        temperature = puw.standardize(temperature)

        if self.temperature is None:
            if is_all(structure_indices):
                self.temperature = deepcopy(temperature)
            else:
                self.temperature = temperature[structure_indices]
        else:
            if is_all(structure_indices):
                self.temperature = np.concatenate([self.temperature, temperature])
            else:
                self.temperature = np.concatenate([self.temperature, temperature[structure_indices]])


    @digest()
    def _append_potential_energy(self, potential_energy, structure_indices='all', skip_digestion=False):

        potential_energy = puw.standardize(potential_energy)

        if self.potential_energy is None:
            if is_all(structure_indices):
                self.potential_energy = deepcopy(potential_energy)
            else:
                self.potential_energy = potential_energy[structure_indices]
        else:
            if is_all(structure_indices):
                self.potential_energy = np.concatenate([self.potential_energy, potential_energy])
            else:
                self.potential_energy = np.concatenate([self.potential_energy, potential_energy[structure_indices]])

    @digest()
    def _append_kinetic_energy(self, kinetic_energy, structure_indices='all', skip_digestion=False):

        kinetic_energy = puw.standardize(kinetic_energy)

        if self.kinetic_energy is None:
            if is_all(structure_indices):
                self.kinetic_energy = deepcopy(kinetic_energy)
            else:
                self.kinetic_energy = kinetic_energy[structure_indices]
        else:
            if is_all(structure_indices):
                self.kinetic_energy = np.concatenate([self.kinetic_energy, kinetic_energy])
            else:
                self.kinetic_energy = np.concatenate([self.kinetic_energy, kinetic_energy[structure_indices]])

    @digest()
    def _append_b_factor(self, b_factor, structure_indices='all', skip_digestion=False):

        b_factor = puw.standardize(b_factor)

        if self.b_factor is None:
            if is_all(structure_indices):
                self.b_factor = deepcopy(b_factor)
            else:
                self.b_factor = b_factor[structure_indices]
        else:
            if is_all(structure_indices):
                self.b_factor = np.concatenate([self.b_factor, b_factor])
            else:
                self.b_factor = np.concatenate([self.b_factor, b_factor[structure_indices]])


    @digest()
    def _append_alternate_location(self, alternate_location, structure_indices='all', skip_digestion=False):

        if self.alternate_location is None:
            if is_all(structure_indices):
                self.alternate_location = deepcopy(alternate_location)
            else:
                self.alternate_location = alternate_location[structure_indices]
        else:
            if is_all(structure_indices):
                self.alternate_location.append(alternate_location)
            else:
                self.alternate_location.append(alternate_location[structure_indices])

    @digest()
    def append(self, structure_id=None, time=None, coordinates=None, velocities=None,
               box=None, temperature=None, potential_energy=None, kinetic_energy=None,
               b_factor=None, alternate_location=None,
               atom_indices='all', structure_indices='all', skip_digestion=False):
        """ Append structures or frames to this object.

             box : pint.Quantity of shape (n_structures, 3, 3)
                The box of the structures

             coordinates : pint.Quantity of shape (n_structures, n_atoms, 3)
                The coordinates of the trajectory for each frame of it in nanometers.

             time :  pint.Quantity of shape (n_structures, )
                The times of the trajectory in picoseconds

        """

        n_structures = None
        n_atoms = None

        if structure_id is not None:

            tmp_n_structures = len(structure_id)
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input attributes have the same number of structures.')

        if time is not None:

            tmp_n_structures = len(time)
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input arguments have the same number of structures to be appended.')

        if coordinates is not None:

            tmp_n_structures = coordinates.shape[0]
            tmp_n_atoms = coordinates.shape[1]
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input arguments have the same number of structures to be appended.')
            if n_atoms is None:
                n_atoms = tmp_n_atoms
            elif n_atoms != tmp_n_atoms:
                raise ValueError('Not all input arguments have the same number of atoms to be appended.')
        
        if velocities is not None:

            tmp_n_structures = velocities.shape[0]
            tmp_n_atoms = velocities.shape[1]
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input arguments have the same number of structures to be appended.')
            if n_atoms is None:
                n_atoms = tmp_n_atoms
            elif n_atoms != tmp_n_atoms:
                raise ValueError('Not all input arguments have the same number of atoms to be appended.')

        if box is not None:

            tmp_n_structures = box.shape[0]
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input arguments have the same number of structures to be appended.')

        if temperature is not None:

            tmp_n_structures = len(temperature)
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input arguments have the same number of structures to be appended.')

        if potential_energy is not None:

            tmp_n_structures = len(potential_energy)
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input arguments have the same number of structures to be appended.')

        if kinetic_energy is not None:

            tmp_n_structures = len(kinetic_energy)
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input arguments have the same number of structures to be appended.')

        if b_factor is not None:

            tmp_n_structures = len(b_factor)
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input arguments have the same number of structures to be appended.')

        if alternate_location is not None:

            tmp_n_structures = len(alternate_location)
            if n_structures is None:
                n_structures = tmp_n_structures
            elif n_structures != tmp_n_structures:
                raise ValueError('Not all input arguments have the same number of structures to be appended.')

        if self.n_structures==0:

            if structure_id is not None:
                self._append_structure_id(structure_id, structure_indices=structure_indices, skip_digestion=True)

            if time is not None:
                self._append_time(time, structure_indices=structure_indices, skip_digestion=True)

            if coordinates is not None:
                self._append_coordinates(coordinates, atom_indices=atom_indices, structure_indices=structure_indices,
                                         skip_digestion=True)

            if velocities is not None:
                self._append_velocities(velocities, atom_indices=atom_indices, structure_indices=structure_indices,
                                        skip_digestion=True)

            if box is not None:
                self._append_box(box, structure_indices=structure_indices, skip_digestion=True)

            if temperature is not None:
                self._append_temperature(temperature, structure_indices=structure_indices, skip_digestion=True)

            if potential_energy is not None:
                self._append_potential_energy(potential_energy, structure_indices=structure_indices,
                                              skip_digestion=True)

            if kinetic_energy is not None:
                self._append_kinetic_energy(kinetic_energy, structure_indices=structure_indices,
                                            skip_digestion=True)

            if b_factor is not None:
                self._append_b_factor(b_factor, structure_indices=structure_indices,
                                      skip_digestion=True)

            if alternate_location is not None:
                self._append_alternate_location(alternate_location, structure_indices=structure_indices,
                                                skip_digestion=True)

        else:

            if (self.structure_id is not None) and (structure_id is not None):
                self._append_structure_id(structure_id, structure_indices=structure_indices,
                                          skip_digestion=True)

            if (self.time is not None) and (time is not None):
                self._append_time(time, structure_indices=structure_indices, skip_digestion=True)

            if (self.coordinates is not None) and (coordinates is not None):
                self._append_coordinates(coordinates, atom_indices=atom_indices,
                                         structure_indices=structure_indices, skip_digestion=True)

            if (self.velocities is not None) and (velocities is not None):
                self._append_velocities(velocities, atom_indices=atom_indices,
                                        structure_indices=structure_indices, skip_digestion=True)

            if (self.box is not None) and (box is not None):
                self._append_box(box, structure_indices=structure_indices, skip_digestion=True)

            if (self.temperature is not None) and (temperature is not None):
                self._append_temperature(temperature, structure_indices=structure_indices, skip_digestion=True)

            if (self.potential_energy is not None) and (potential_energy is not None):
                self._append_potential_energy(potential_energy, structure_indices=structure_indices)

            if (self.kinetic_energy is not None) and (kinetic_energy is not None):
                self._append_kinetic_energy(kinetic_energy, structure_indices=structure_indices, 
                                            skip_digestion=True)

            if (self.b_factor is not None) and (kinetic_energy is not None):
                self._append_b_factor(b_factor, structure_indices=structure_indices, 
                                            skip_digestion=True)

            if (self.alternate_location is not None) and (alternate_location is not None):
                self._append_alternate_location(alternate_location, structure_indices=structure_indices, 
                                            skip_digestion=True)

        if n_structures is None:
            n_structures = 0
        if n_atoms is None:
            n_atoms = 0

        if self.n_structures==0 and self.n_atoms==0:
            self.n_structures = n_structures
            self.n_atoms = n_atoms
        else:
            self.n_structures += n_structures


    @digest(form='molsysmt.Structures')
    def append_structures(self, item, atom_indices='all', structure_indices='all', skip_digestion=False):

        if is_all(atom_indices) and is_all(structure_indices):

            self.append(structure_id=item.structure_id,
                        time=item.time,
                        coordinates=item.coordinates,
                        velocities=item.velocities,
                        box=item.box,
                        temperature=item.temperature,
                        potential_energy=item.potential_energy,
                        kinetic_energy=item.kinetic_energy,
                        alternate_location=item.alternate_location,
                        skip_digestion=True
                       )

        else:

            raise NotImplementedError

    @digest(form='molsysmt.Structures')
    def add(self, item, atom_indices='all', structure_indices='all', skip_digestion=False):

        if is_all(structure_indices):
            if self.n_structures!=item.n_structures:
                raise ValueError('Both items need to have the same n_structures')
        elif self.n_structures!=len(structure_indices):
            raise ValueError('Both items need to have the same n_structures')

        if item.coordinates is not None:
            if self.coordinates is None:
                if is_all(structure_indices):
                    if is_all(atom_indices):
                        self.coordinates = deepcopy(item.coordinates)
                    else:
                        self.coordinates = item.coordinates[:,atom_indices,:]
                else:
                    if is_all(atom_indices):
                        self.coordinates = item.coordinates[structure_indices,:,:]
                    else:
                        self.coordinates = item.coordinates[np.ix_(structure_indices, atom_indices)]
            else:
                if is_all(structure_indices):
                    if is_all(atom_indices):
                        value_self_coordinates, unit = puw.get_value_and_unit(self.coordinates)
                        value_coordinates = puw.get_value(item.coordinates, to_unit=unit)
                        self.coordinates = np.hstack([value_self_coordinates, value_coordinates])*unit
                    else:
                        value_self_coordinates, unit = puw.get_value_and_unit(self.coordinates)
                        value_coordinates = puw.get_value(item.coordinates[:,atom_indices,:], to_unit=unit)
                        self.coordinates = np.hstack([value_self_coordinates, value_coordinates])*unit
                else:
                    if is_all(atom_indices):
                        value_self_coordinates, unit = puw.get_value_and_unit(self.coordinates)
                        value_coordinates = puw.get_value(item.coordinates[structure_indices,:,:], to_unit=unit)
                        self.coordinates = np.hstack([value_self_coordinates, value_coordinates])*unit
                    else:
                        value_self_coordinates, unit = puw.get_value_and_unit(self.coordinates)
                        value_coordinates = puw.get_value(item.coordinates[np.ix_(structure_indices, atom_indices)],
                                                          to_unit=unit)
                        self.coordinates = np.hstack([value_self_coordinates, value_coordinates])*unit
 
        if item.velocities is not None:
            if self.velocities is None:
                if is_all(structure_indices):
                    if is_all(atom_indices):
                        self.velocities = deepcopy(item.velocities)
                    else:
                        self.velocities = item.velocities[:,atom_indices,:]
                else:
                    if is_all(atom_indices):
                        self.velocities = item.velocities[structure_indices,:,:]
                    else:
                        self.velocities = item.velocities[np.ix_(structure_indices, atom_indices)]
            else:
                if is_all(structure_indices):
                    if is_all(atom_indices):
                        value_self_velocities, unit = puw.get_value_and_unit(self.velocities)
                        value_velocities = puw.get_value(item.velocities, to_unit=unit)
                        self.velocities = np.hstack([value_self_velocities, value_velocities])*unit
                    else:
                        value_self_velocities, unit = puw.get_value_and_unit(self.velocities)
                        value_velocities = puw.get_value(item.velocities[:,atom_indices,:], to_unit=unit)
                        self.velocities = np.hstack([value_self_velocities, value_velocities])*unit
                else:
                    if is_all(atom_indices):
                        value_self_velocities, unit = puw.get_value_and_unit(self.velocities)
                        value_velocities = puw.get_value(item.velocities[structure_indices,:,:], to_unit=unit)
                        self.velocities = np.hstack([value_self_velocities, value_velocities])*unit
                    else:
                        value_self_velocities, unit = puw.get_value_and_unit(self.velocities)
                        value_velocities = puw.get_value(item.velocities[np.ix_(structure_indices, atom_indices)],
                                                          to_unit=unit)
                        self.velocities = np.hstack([value_self_velocities, value_velocities])*unit

        if self.coordinates is not None:
            self.n_atoms = self.coordinates.shape[1]
        elif self.velocities is not None:
            self.n_atoms = self.velocities.shape[1]


    @digest()
    def extract(self, atom_indices='all', structure_indices='all', copy_if_all=False, skip_digestion=False):
        """ Returns a new Structures object with the specified atoms and/or
            structures.

            Parameters
            ----------
            atom_indices : str or arraylike of int, default='all'
                The indices of the extracted atoms.

            structure_indices : str or arraylike of int, default='all'
                The indices of the extracted structures or frames.

            Returns
            -------
            Structures
                The new structures object with the extracted atoms and frames.
        """
        if is_all(atom_indices) and is_all(structure_indices):

            if copy_if_all:

                return self.copy()

            else:

                return self

        else:


            if self.structure_id is None:
                structure_id = None
            else:
                if is_all(structure_indices):
                    structure_id = deepcopy(self.structure_id)
                else:
                    structure_id = self.structure_id[structure_indices]

            if self.time is None:
                time = None
            else:
                if is_all(structure_indices):
                    time = deepcopy(self.time)
                else:
                    time = self.time[structure_indices]

            if self.box is None:
                box = None
            else:
                if is_all(structure_indices):
                    box = deepcopy(self.box)
                else:
                    box = self.box[structure_indices]

            if self.temperature is None:
                temperature = None
            else:
                if is_all(structure_indices):
                    temperature = deepcopy(self.temperature)
                else:
                    temperature = self.temperature[structure_indices]

            if self.potential_energy is None:
                potential_energy = None
            else:
                if is_all(structure_indices):
                    potential_energy = deepcopy(self.potential_energy)
                else:
                    potential_energy = self.potential_energy[structure_indices]

            if self.kinetic_energy is None:
                kinetic_energy = None
            else:
                if is_all(structure_indices):
                    kinetic_energy = deepcopy(self.kinetic_energy)
                else:
                    kinetic_energy = self.kinetic_energy[structure_indices]

            if self.coordinates is None:
                coordinates = None
            else:
                if is_all(structure_indices):
                    if is_all(atom_indices):
                        coordinates = deepcopy(self.coordinates)
                    else:
                        coordinates = self.coordinates[:,atom_indices,:]
                else:
                    if is_all(atom_indices):
                        coordinates = self.coordinates[structure_indices,:,:]
                    else:
                        coordinates = self.coordinates[np.ix_(structure_indices, atom_indices)]

            if self.velocities is None:
                velocities = None
            else:
                if is_all(structure_indices):
                    if is_all(atom_indices):
                        velocities = deepcopy(self.velocities)
                    else:
                        velocities = self.velocities[:,atom_indices,:]
                else:
                    if is_all(atom_indices):
                        velocities = self.velocities[structure_indices,:,:]
                    else:
                        velocities = self.velocities[np.ix_(structure_indices, atom_indices)]

            if self.alternate_location is None:
                alternate_location = None
            else:
                if is_all(structure_indices):
                    if is_all(atom_indices):
                        alternate_location = deepcopy(self.alternate_location)
                    else:
                        alternate_location = []
                        for tmp_alt_loc in self.alternate_location:
                            aux_dict={}
                            for tmp_atom_index in tmp_alt_loc.keys():
                                if tmp_atom_index in atom_indices:
                                    new_atom_index = np.argwhere(atom_indices == tmp_atom_index)[0][0]
                                    aux_dict[new_atom_index] = tmp_alt_loc[tmp_atom_index]
                            alternate_location.append(aux_dict)
                else:
                    if is_all(atom_indices):
                        alternate_location = [self.alternate_location[ii] for ii in structure_indices]
                    else:
                        aux_alternate_location = [self.alternate_location[ii] for ii in structure_indices]
                        alternate_location = []
                        for tmp_alt_loc in aux_alternate_location:
                            aux_dict={}
                            for tmp_atom_index in tmp_alt_loc.keys():
                                if tmp_atom_index in atom_indices:
                                    new_atom_index = np.where(atom_indices == tmp_atom_index)[0]
                                    aux_dict[new_atom_index] = tmp_alt_loc[tmp_atom_index]
                            alternate_location.append(aux_dict)
                        del(aux_alternate_location)

        return Structures(structure_id=structure_id,
                          time=time,
                          coordinates=coordinates,
                          velocities=velocities,
                          box=box,
                          temperature=temperature,
                          potential_energy=potential_energy,
                          kinetic_energy=kinetic_energy,
                          alternate_location=alternate_location,
                          skip_digestion=True
                          )


    def copy(self):
        """ Returns a copy of the structures."""
        return deepcopy(self)

