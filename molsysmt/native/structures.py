from copy import deepcopy
import numpy as np
from molsysmt import puw
from molsysmt._private.variables import is_all
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

    def __init__(self, step=None, time=None, coordinates=None, box=None):

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

        self.file = None

    @staticmethod
    def _concatenate_arrays(array_1, array_2, name):
        """ Concatenates two arrays provided that they are not null."""
        if array_2 is not None:
            if array_1 is None:
                raise ValueError(f"The trajectory has no {name} array to append the new frame.")
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
                raise ValueError("The coordinates to be appended in the system needs to have the same number of atoms.")

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
        """
        if is_all(atom_indices) and is_all(structure_indices):
            return self.copy()

        else:

            tmp_item = Structures()

            if self.step is not None:
                if not is_all(structure_indices):
                    tmp_item.step = self.step[structure_indices]
                else:
                    tmp_item.step = deepcopy(self.step)

            if self.time is not None:
                if not is_all(structure_indices):
                    tmp_item.time = self.time[structure_indices]
                else:
                    tmp_item.time = deepcopy(self.time)

            if self.box is not None:
                if not is_all(structure_indices):
                    tmp_item.box = self.box[structure_indices]
                else:
                    tmp_item.box = deepcopy(self.box)

            if not is_all(atom_indices):
                tmp_item.coordinates = self.coordinates[:, atom_indices, :]
            else:
                tmp_item.coordinates = deepcopy(self.coordinates)

            if not is_all(structure_indices):
                tmp_item.coordinates = tmp_item.coordinates[structure_indices, :, :]

            tmp_item.n_structures = tmp_item.coordinates.shape[0]
            tmp_item.n_atoms = tmp_item.coordinates.shape[1]

            if self.file is not None:
                tmp_item.file = self.file.copy()

        return tmp_item

    def add(self, item, selection='all', structure_indices='all'):

        from molsysmt.basic import get

        step, time, box = get(item, element="system", structure_indices=structure_indices, step=True, time=True,
                              box=True)
        coordinates = get(item, element="atom", selection=selection, structure_indices=structure_indices,
                          coordinates=True)

        if self.n_structures == 0:
            self.append_structures(step, time, coordinates, box)
        else:
            if self.n_structures != coordinates.shape[0]:
                raise ValueError('Both items need to have the same n_structures')
            else:
                unit = puw.get_unit(self.coordinates)
                value_coordinates = puw.get_value(coordinates, to_unit=unit)
                value_self_coordinates = puw.get_value(self.coordinates)
                self.coordinates = np.hstack([value_self_coordinates, value_coordinates]) * unit
                del (value_coordinates, value_self_coordinates)

        self.n_atoms = self.coordinates.shape[1]

    def append(self, item, selection='all', structure_indices='all'):

        from molsysmt.basic import get

        step, time, coordinate, box = get(item, element="atom", selection=selection,
                                          structure_indices=structure_indices, frame=True)
        self.append_structures(step, time, coordinate, box)

    def copy(self):
        """ Returns a copy of the structures."""
        return deepcopy(self)
