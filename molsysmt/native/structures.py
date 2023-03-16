from copy import deepcopy
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from molsysmt.basic import get
from molsysmt.pbc import get_lengths_and_angles_from_box
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

        structure_id :


    """

    @digest()
    def __init__(self, structure_id=None, time=None, coordinates=None, velocities=None, box=None):

        self.structure_id = structure_id
        self.time = time
        self.coordinates = coordinates
        self.velocities = velocities
        self.box = box
        self.occupancy = None
        self.alternate_location = None
        self.b_factor = None

        if coordinates is not None:
            self.n_structures = coordinates.shape[0]
            self.n_atoms = coordinates.shape[1]
        else:
            self.n_structures = 0
            self.n_atoms = 0

        self._current_structure = 0

    @staticmethod
    def _concatenate_arrays(array_1, array_2, name):
        """ Concatenates two arrays provided that they are not null."""
        if array_2 is not None:
            if array_1 is None:
                raise ValueError(
                    f"The trajectory has no {name} array to append the new frame.")
            else:
                return np.concatenate([array_1, array_2])

    @digest()
    def append_structures(self, structure_id=None, time=None, coordinates=None, velocities=None, box=None):
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

        if self.n_structures == 0:

            self.coordinates = coordinates
            self.velocities = velocities
            self.structure_id = structure_id
            self.time = time
            self.box = box
            self.n_structures = n_structures
            self.n_atoms = n_atoms

        else:

            if n_atoms != self.n_atoms:
                raise ValueError(
                    "The coordinates to be appended in the system "
                    "need to have the same number of atoms.")

            self.structure_id = self._concatenate_arrays(self.structure_id, structure_id, "structure_ids")
            self.time = self._concatenate_arrays(self.time, time, "time")
            self.box = self._concatenate_arrays(self.box, box, "structure_ids")

            self.coordinates = np.concatenate([self.coordinates, coordinates])
            self.velocities = np.concatenate([self.velocities, velocities])
            self.n_structures += n_structures

    def get_box_lengths(self):


        if self.box is not None:
            lengths, _ = get_lengths_and_angles_from_box(self.box)
        else:
            lengths = None

        return lengths

    def get_box_angles(self):

        if self.box is not None:
            _, angles = get_lengths_and_angles_from_box(self.box)
        else:
            _, angles = None

        return angles

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

            if not is_all(atom_indices):
                coordinates = self.coordinates[:, atom_indices, :]
            else:
                coordinates = deepcopy(self.coordinates)

            if not is_all(atom_indices):
                velocities = self.velocities[:, atom_indices, :]
            else:
                velocities = deepcopy(self.velocities)

            if not is_all(structure_indices):
                coordinates = coordinates[structure_indices, :, :]

        return Structures(structure_id=structure_id,
                          time=time,
                          coordinates=coordinates,
                          velocities=velocities,
                          box=box,
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

        structure_id, time, box = get(item,
                              element="system",
                              structure_indices=structure_indices,
                              structure_id=True,
                              time=True,
                              box=True,
                              )
        coordinates = get(item,
                          element="atom",
                          selection=selection,
                          structure_indices=structure_indices,
                          coordinates=True,
                          )

        coordinates = get(item,
                          element="atom",
                          selection=selection,
                          structure_indices=structure_indices,
                          velocities=True,
                          )

        if self.n_structures == 0:
            self.append_structures(structure_id, time, coordinates, box)
        else:
            if self.n_structures != coordinates.shape[0]:
                raise ValueError('Both items need to have the same n_structures')
            unit = puw.get_unit(self.coordinates)
            value_coordinates = puw.get_value(coordinates, to_unit=unit)
            value_self_coordinates = puw.get_value(self.coordinates)
            self.coordinates = np.hstack([value_self_coordinates, value_coordinates]) * unit
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

    def get_structure_data(self, structure, selection="all", chunk_size=1):
        """ Returns the structure_ids, time, coordinates and box of the
            given structure

            Parameters
            ----------
            structure : int
                The index of the structure

            selection : arraylike of int, default="all"
                The indices of the selected atoms.

            chunk_size : int, default=1
                Amount of structures to return in each of the arrays.

            Returns
            -------
            box : pint.Quantity of shape (3, 3)
                The box of the structure. If chunk_size is greater than one
                the shape will be (chunk_size, 3, 3)

            coordinates : pint.Quantity of shape (n_atoms, 3)
                The coordinates of the structure. If chunk_size is greater than one
                the shape will be (chunk_size, n_atoms, 3)

            time :  pint.Quantity
                The times of the structure. If chunk_size is greater than one
                the shape will be (chunk_size,)
        """
        structure_end = structure + chunk_size

        if self.structure_id is not None:
            structure_id = self.structure_id[structure: structure_end]
        else:
            structure_id = None

        if self.time is not None:
            time = self.time[structure: structure_end]
        else:
            time = None

        if self.coordinates is not None:
            if is_all(selection):
                # If chunk size is 1 we return a 2D array. If not coordinates will
                # be a 3D array
                if chunk_size == 1:
                    coordinates = self.coordinates[structure]
                else:
                    coordinates = self.coordinates[structure: structure_end]
            else:
                if chunk_size == 1:
                    coordinates = self.coordinates[structure, selection, :]
                else:
                    coordinates = self.coordinates[structure: structure_end, selection, :]
        else:
            coordinates = None

        if self.velocities is not None:
            if is_all(selection):
                if chunk_size == 1:
                    velocities = self.velocities[structure]
                else:
                    velocities = self.velocities[structure: structure_end]
            else:
                if chunk_size == 1:
                    velocities = self.velocities[structure, selection, :]
                else:
                    velocities = self.velocities[structure: structure_end, selection, :]
        else:
            velocities = None

        if self.box is not None:
            if chunk_size == 1:
                box = self.box[structure]
            else:
                box = self.box[structure: structure_end]
        else:
            box = None

        return structure_id, time, coordinates, velocities, box

    def _iterate_structures(self, start=0, stop=None,
                            interval=1, selection="all", chunk_size=1):
        """ Helper function for the iterate method."""
        self._current_structure = start
        while self._current_structure < self.n_structures:
            if self._current_structure >= stop:
                break

            yield self.get_structure_data(self._current_structure,
                                          selection,
                                          chunk_size)

            if chunk_size > 1:
                self._current_structure += chunk_size
            else:
                self._current_structure += interval

    def iterate(self, start=0, stop=None,
                interval=1, selection="all", chunk_size=1):
        """ Generator to iterate over the structure_ids, time, coordinates and box
            of each structure (frame).

            Parameters
            ----------
            start: int
                First structure index of the trajectory to start with.

            stop: int, default=None
                The iteration finishes if the current structure index
                is larger than or equal to this integer.

            interval : int, default=1
                Number of structure indices to skip in each iteration

            selection : arraylike of int or 'all', default='all'
                The indices of the selected atoms.

            chunk_size : int, default=1
                Amount of structures in the output of each iteration.

            Yields
            ------
            structure_id :

            box : pint.Quantity of shape (3, 3)
                The box of the structure

            coordinates : pint.Quantity of shape (n_atoms, 3)
                The coordinates of the structure.

            time :  pint.Quantity
                The times of the structure

        """
        if start < 0 or start >= self.n_structures:
            raise IteratorError(
                f"Start should be > 0 and < {self.n_structures}"
            )

        if interval < 1 or interval > self.n_structures:
            raise IteratorError(
                f"Interval should be > 0 and < {self.n_structures}"
            )

        if chunk_size < 1 or chunk_size > self.n_structures:
            raise IteratorError(
                f"Chunk size should be > 0 and < {self.n_structures}")

        if interval != 1 and chunk_size != 1:
            # We cannot have an interval and a chunk size greater than 1 simultaneously
            raise IteratorError(
                "Chunk size and interval cannot be greater than one simultaneously.")

        if stop is None:
            stop = self.n_structures

        if stop < 1 or stop > self.n_structures:
            raise IteratorError(
                f"Stop should be > 0 and < {self.n_structures}"
            )

        return self._iterate_structures(start, stop, interval, selection, chunk_size)

    def copy(self):
        """ Returns a copy of the structures."""
        return deepcopy(self)

    def __iter__(self):
        self._current_structure = -1
        return self

    def __next__(self):
        """ Iterate through the structure_ids, time, coordinates and box
            of each structure (frame).
        """
        self._current_structure += 1
        if self._current_structure >= self.n_structures:
            raise StopIteration

        return self.get_structure_data(self._current_structure)
