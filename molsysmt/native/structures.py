from copy import deepcopy
import numpy as np
from molsysmt import puw
from molsysmt._private.variables import is_all
import molsysmt._private.exceptions.value_errors as exc
from molsysmt.basic import get
from molsysmt.pbc import box_lengths_from_box_vectors, box_angles_from_box_vectors


class Structures:
    """ Class to store the trajectory data of a molecular system


        Attributes
        ----------
        box : pint.Quantity of shape (n_structures, 3, 3)
            The box of the molecular system in nanometers.

        coordinates : pint.Quantity of shape (n_structures, n_atoms, 3)
            The coordinates of the trajectory for each frame of it in nanometers.

        n_atoms : int
            Number of atoms in the trajectory.

        n_structures : int
            Number of structures or frames in the trajectory.

        time :  pint.Quantity of shape (n_structures, )
            The times of the trajectory in picoseconds.

        step :


    """

    def __init__(self, step=None, time=None, coordinates=None, box=None, file=None):

        self.step = step
        self.time = time
        self.coordinates = coordinates
        self.box = box

        if coordinates is not None:
            self.n_structures = coordinates.shape[0]
            self.n_atoms = coordinates.shape[1]
        else:
            self.n_structures = 0
            self.n_atoms = 0

        self.file = file
        self._current_structure = 0

    @staticmethod
    def _concatenate_arrays(array_1, array_2, name):
        """ Concatenates two arrays provided that they are not null."""
        if array_2 is not None:
            if array_1 is None:
                raise exc.ConcatenationError(
                    f"The trajectory has no {name} array to append the new frame.")
            else:
                return np.concatenate([array_1, array_2])

    def append_structures(self, step=None, time=None, coordinates=None, box=None, check=False):
        """ Append structures or frames to this object.

             box : pint.Quantity of shape (n_structures, 3, 3)
                The box of the structures

             coordinates : pint.Quantity of shape (n_structures, n_atoms, 3)
                The coordinates of the trajectory for each frame of it in nanometers.

             time :  pint.Quantity of shape (n_structures, )
                The times of the trajectory in picoseconds

        """
        # TODO: check argument is not used
        if step is not None and not isinstance(step, (list, np.ndarray)):
            step = np.array([step])

        if time is not None:
            time = puw.standardize(time)
        if coordinates is not None:
            coordinates = puw.standardize(coordinates)
        if box is not None:
            box = puw.standardize(box)

        n_structures = coordinates.shape[0]
        n_atoms = coordinates.shape[1]

        if self.n_structures == 0:

            self.coordinates = coordinates
            self.step = step
            self.time = time
            self.box = box
            self.n_structures = n_structures
            self.n_atoms = n_atoms

        else:

            if n_atoms != self.n_atoms:
                raise exc.IncorrectShapeError(
                    "The coordinates to be appended in the system "
                    "need to have the same number of atoms.")

            self.step = self._concatenate_arrays(self.step, step, "steps")
            self.time = self._concatenate_arrays(self.time, time, "time")
            self.box = self._concatenate_arrays(self.box, box, "steps")

            self.coordinates = np.concatenate([self.coordinates, coordinates])
            self.n_structures += n_structures

    def get_box_lengths(self):
        """ Returns the lengths of the box."""
        if self.box is not None:
            return box_lengths_from_box_vectors(self.box)
        return

    def get_box_angles(self):
        """ Returns the angles of the box."""
        if self.box is not None:
            return box_angles_from_box_vectors(self.box)
        return

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

            if self.step is not None and extract_structures:
                step = self.step[structure_indices]
            else:
                step = deepcopy(self.step)

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

            if not is_all(structure_indices):
                coordinates = coordinates[structure_indices, :, :]

            if self.file is not None:
                file = self.file.copy()
            else:
                file = None

        return Structures(step=step,
                          time=time,
                          coordinates=coordinates,
                          box=box,
                          file=file
                          )

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

        step, time, box = get(item,
                              element="system",
                              structure_indices=structure_indices,
                              step=True,
                              time=True,
                              box=True)
        coordinates = get(item,
                          element="atom",
                          selection=selection,
                          structure_indices=structure_indices,
                          coordinates=True)

        if self.n_structures == 0:
            self.append_structures(step, time, coordinates, box)
        else:
            if self.n_structures != coordinates.shape[0]:
                raise ValueError('Both items need to have the same n_structures')
            unit = puw.get_unit(self.coordinates)
            value_coordinates = puw.get_value(coordinates, to_unit=unit)
            value_self_coordinates = puw.get_value(self.coordinates)
            self.coordinates = np.hstack([value_self_coordinates, value_coordinates]) * unit

        self.n_atoms = self.coordinates.shape[1]

    def append(self, item, selection='all', structure_indices='all'):
        """ Appends the step, time coordinates and box of the given item to this.

            Parameters
            ----------
            item : MolecularSystem
                The molecular system that will be appended.

            selection : str or arraylike of int, default='all'
                Selects only these atoms from the given item.

            structure_indices : str or arraylike of int, default='all'
                Select only these structures from the given item
        """

        step, time, coordinates, box = get(item,
                                           selection=selection,
                                           structure_indices=structure_indices,
                                           step=True,
                                           time=True,
                                           coordinates=True,
                                           box=True
                                           )
        self.append_structures(step, time, coordinates, box)

    def get_structure_data(self, structure, selection="all", chunk_size=1):
        """ Returns the steps, time, coordinates and box of the
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

        if self.step is not None:
            step = self.step[structure: structure_end]
        else:
            step = None

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

        if self.box is not None:
            if chunk_size == 1:
                box = self.box[structure]
            else:
                box = self.box[structure: structure_end]
        else:
            box = None

        return step, time, coordinates, box

    def iterate(self, start=0, stop=None,
                interval=1, selection="all", chunk_size=1):
        """ Generator to iterate over the steps, time, coordinates and box
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
            step :

            box : pint.Quantity of shape (3, 3)
                The box of the structure

            coordinates : pint.Quantity of shape (n_atoms, 3)
                The coordinates of the structure.

            time :  pint.Quantity
                The times of the structure

        """
        # TODO: argument checking is done in every iteration. It should be moved
        #  to a different method.
        if start < 0 or start >= self.n_structures:
            raise exc.IteratorStartError(
                f"Start should be > 0 and < {self.n_structures}"
            )

        if interval < 1 or interval > self.n_structures:
            raise exc.IteratorIntervalError(
                f"Interval should be > 0 and < {self.n_structures}"
            )

        if chunk_size < 1 or chunk_size > self.n_structures:
            raise exc.IteratorChunkSizeError(
                f"Chunk size should be > 0 and < {self.n_structures}")

        if interval != 1 and chunk_size != 1:
            # We cannot have an interval and a chunk size greater than 1 simultaneously
            raise exc.IteratorChunkSizeError(
                "Chunk size and interval cannot be greater than one simultaneously.")

        if stop is None:
            stop = self.n_structures

        if stop < 1 or stop > self.n_structures:
            raise exc.IteratorStopError(
                f"Stop should be > 0 and < {self.n_structures}"
            )

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

    def copy(self):
        """ Returns a copy of the structures."""
        return deepcopy(self)

    def __iter__(self):
        self._current_structure = -1
        return self

    def __next__(self):
        """ Iterate through the steps, time, coordinates and box
            of each structure (frame).
        """
        self._current_structure += 1
        if self._current_structure >= self.n_structures:
            raise StopIteration

        return self.get_structure_data(self._current_structure)
