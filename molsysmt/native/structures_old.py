from copy import deepcopy
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from molsysmt.basic import get
from molsysmt._private.exceptions import IteratorError
from molsysmt._private.digestion import digest

class StructuresOld:
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

        structure_id :


    """

    @digest()
    def __init__(self, structure_id=None, time=None, coordinates=None, velocities=None, box=None,
            occupancy=None, b_factor=None, alternate_location=None, bioassembly=None,
            temperature=None, potential_energy=None, kinetic_energy=None):

        self.structure_id = structure_id
        self.time = time
        self.coordinates = coordinates
        self.velocities = velocities
        self.box = box
        self.occupancy = occupancy
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

    @staticmethod
    def _concatenate_arrays(array_1, array_2):
        """ Concatenates two arrays provided that they are not null."""
        if array_2 is not None:
            if array_1 is None:
                raise ValueError(
                    f"The trajectory has no array to append the new frame.")
            else:
                return np.concatenate([array_1, array_2])

    @digest()
    def append_structures(self, structure_id=None, time=None, coordinates=None, velocities=None,
            box=None, temperature=None, potential_energy=None, kinetic_energy=None):
        """ Append structures or frames to this object.

             box : pint.Quantity of shape (n_structures, 3, 3)
                The box of the structures

             coordinates : pint.Quantity of shape (n_structures, n_atoms, 3)
                The coordinates of the trajectory for each frame of it in nanometers.

             time :  pint.Quantity of shape (n_structures, )
                The times of the trajectory in picoseconds

        """

        n_structures = 0
        n_atoms = 0

        if structure_id is not None and not isinstance(structure_id, (list, np.ndarray)):
            structure_id = np.array([structure_id])

        if time is not None:
            time = puw.standardize(time)
        if coordinates is not None:
            coordinates = puw.standardize(coordinates)
            n_structures = coordinates.shape[0]
            n_atoms = coordinates.shape[1]
        if velocities is not None:
            velocities = puw.standardize(velocities)
        if box is not None:
            box = puw.standardize(box)
        if temperature is not None:
            temperature = puw.standardize(temperature)
        if potential_energy is not None:
            potential_energy = puw.standardize(potential_energy)
        if kinetic_energy is not None:
            kinetic_energy = puw.standardize(kinetic_energy)

        if self.n_structures == 0:

            self.coordinates = coordinates
            self.velocities = velocities
            self.structure_id = structure_id
            self.time = time
            self.box = box
            self.temperature = temperature
            self.potential_energy = potential_energy
            self.kinetic_energy = kinetic_energy
            self.n_structures = n_structures
            self.n_atoms = n_atoms

        else:

            if n_atoms != self.n_atoms:
                raise ValueError(
                    "The coordinates to be appended in the system "
                    "need to have the same number of atoms.")

            self.structure_id = self._concatenate_arrays(self.structure_id, structure_id)
            self.time = self._concatenate_arrays(self.time, time)
            self.box = self._concatenate_arrays(self.box, box)
            self.temperature = self._concatenate_arrays(self.temperature, temperature)
            self.potential_energy = self._concatenate_arrays(self.potential_energy,
                    potential_energy)
            self.kinetic_energy = self._concatenate_arrays(self.kinetic_energy,
                    kinetic_energy)

            self.coordinates = self._concatenate_arrays(self.coordinates, coordinates)
            self.velocities = self._concatenate_arrays(self.velocities, velocities)
            self.n_structures += n_structures

    @digest()
    def extract(self, atom_indices='all', structure_indices='all'):
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
            return self.copy()

        else:

            extract_structures = not is_all(structure_indices)

            if self.structure_id is not None and extract_structures:
                structure_id = self.structure_id[structure_indices]
            else:
                structure_id = deepcopy(self.structure_id)

            if self.time is not None and extract_structures:
                time = self.time[structure_indices]
            else:
                time = deepcopy(self.time)

            if self.box is not None and extract_structures:
                box = self.box[structure_indices]
            else:
                box = deepcopy(self.box)

            if self.temperature is not None and extract_structures:
                temperature = self.temperature[structure_indices]
            else:
                temperature = deepcopy(self.temperature)

            if self.potential_energy is not None and extract_structures:
                potential_energy = self.potential_energy[structure_indices]
            else:
                potential_energy = deepcopy(self.potential_energy)

            if self.kinetic_energy is not None and extract_structures:
                kinetic_energy = self.kinetic_energy[structure_indices]
            else:
                kinetic_energy = deepcopy(self.kinetic_energy)

            if self.coordinates is not None:
                if not is_all(atom_indices):
                    coordinates = self.coordinates[:, atom_indices, :]
                else:
                    coordinates = deepcopy(self.coordinates)
                if not is_all(structure_indices):
                    coordinates = coordinates[structure_indices, :, :]
            else:
                coordinates = None

            if self.velocities is not None:
                if not is_all(atom_indices):
                    velocities = self.velocities[:, atom_indices, :]
                else:
                    velocities = deepcopy(self.velocities)
                if not is_all(structure_indices):
                    velocities = velocities[structure_indices, :, :]
            else:
                velocities = None

        return Structures(structure_id=structure_id,
                          time=time,
                          coordinates=coordinates,
                          velocities=velocities,
                          box=box,
                          temperature=temperature,
                          potential_energy=potential_energy,
                          kinetic_energy=kinetic_energy
                          )


    @digest()
    def add(self, item, selection='all', structure_indices='all'):
        """ Adds the coordinates of another item to this.

            Parameters
            ----------

            item : MolecularSystem
                The molecular system whose coordinates will be added.

            selection : str or arraylike of int, default='all'
                Selects only these atoms from the given item.

            structure_indices : str or arraylike of int, default='all'
                Select only these structures from the given item

        """



        n_structures = get(item,
                           element="system",
                           structure_indices=structure_indices,
                           n_structures=True,
                           )

        coordinates = get(item,
                          element="atom",
                          selection=selection,
                          structure_indices=structure_indices,
                          coordinates=True,
                          )

        velocities = get(item,
                          element="atom",
                          selection=selection,
                          structure_indices=structure_indices,
                          velocities=True,
                          )

        if self.n_structures != n_structures:
            raise ValueError('Both items need to have the same n_structures')

        if (self.coordinates is None) or (coordinates is None):
            self.coordinates = None
        else:
            unit = puw.get_unit(self.coordinates)
            value_coordinates = puw.get_value(coordinates, to_unit=unit)
            value_self_coordinates = puw.get_value(self.coordinates)
            self.coordinates = np.hstack([value_self_coordinates, value_coordinates]) * unit

        if (self.velocities is None) or (velocities is None):
            self.velocities = None
        else:
            unit = puw.get_unit(self.velocities)
            value_velocities = puw.get_value(velocities, to_unit=unit)
            value_self_velocities = puw.get_value(self.velocities)
            self.velocities = np.hstack([value_self_velocities, value_velocities]) * unit

        self.n_atoms = self.coordinates.shape[1]

    @digest()
    def append(self, item, selection='all', structure_indices='all'):
        """ Appends the structure_id, time coordinates and box of the given item to this.

            Parameters
            ----------
            item : MolecularSystem
                The molecular system that will be appended.

            selection : str or arraylike of int, default='all'
                Selects only these atoms from the given item.

            structure_indices : str or arraylike of int, default='all'
                Select only these structures from the given item
        """

        structure_id, time, coordinates, velocities, box = get(item,
                                           selection=selection,
                                           structure_indices=structure_indices,
                                           structure_id=True,
                                           time=True,
                                           coordinates=True,
                                           velocities=True,
                                           box=True,
                                           )

        self.append_structures(structure_id, time, coordinates, velocities, box)


    def copy(self):
        """ Returns a copy of the structures."""
        return deepcopy(self)

