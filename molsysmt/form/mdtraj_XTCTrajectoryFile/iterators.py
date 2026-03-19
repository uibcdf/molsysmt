from molsysmt._private.smonitor import NotImplementedIteratorError
from molsysmt._private.variables import is_all
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.indices import indices_iterator
from molsysmt import pyunitwizard as puw
import numpy as np


class StructuresIterator():

    @arg_digest(form='mdtraj.XTCTrajectoryFile')
    def __init__(self, molecular_system, atom_indices='all', start=0, stop=None, step=1, chunk=1,
            structure_indices=None, output_type='values', skip_digestion=False, **kwargs):

        self.molecular_system = molecular_system
        self.atom_indices = atom_indices
        self.structure_indices = structure_indices
        self.start = start
        self.step = step
        self.stop = stop
        self.chunk = chunk

        self.arguments = []
        self._output_dictionary = {}
        self._output_type = output_type

        for key, val in kwargs.items():
            if val:
                self.arguments.append(key)
                self._output_dictionary[key] = None

        if is_all(structure_indices):
            structure_indices = None

        if self.stop is None:
            if structure_indices is None:
                from .get_structural_attributes import get_n_structures_from_system
                self.stop = get_n_structures_from_system(molecular_system, skip_digestion=True)
            else:
                self.stop = len(structure_indices)

        self._indices_iterator = indices_iterator(indices=structure_indices, start=self.start,
                stop=self.stop, step=self.step, chunk=self.chunk)

        self._mdtraj_atom_indices = None if is_all(self.atom_indices) else self.atom_indices

    def __iter__(self):

        return self

    def __next__(self):

        indices = self._indices_iterator.__next__()

        if indices is not None:

            idx_array = np.atleast_1d(np.array(indices))
            coords_list = []
            box_list = []
            time_list = []

            for ii in idx_array:
                self.molecular_system.seek(int(ii))
                xyz, time, step, box = self.molecular_system.read(1,
                        atom_indices=self._mdtraj_atom_indices)
                coords_list.append(np.float64(xyz[0]))
                box_list.append(np.float64(box[0]))
                time_list.append(np.float64(time[0]))

            for argument in self.arguments:

                if argument == 'coordinates':
                    self._output_dictionary['coordinates'] = puw.quantity(
                            np.array(coords_list), 'nanometer', standardized=True)

                elif argument == 'box':
                    self._output_dictionary['box'] = puw.quantity(
                            np.array(box_list), 'nanometer', standardized=True)

                elif argument == 'time':
                    self._output_dictionary['time'] = puw.quantity(
                            np.array(time_list), 'picosecond', standardized=True)

                elif argument == 'structure_id':
                    self._output_dictionary['structure_id'] = idx_array

            if self._output_type == 'values':
                output = list(self._output_dictionary.values())
                if len(output) == 1:
                    output = output[0]
            elif self._output_type == 'dictionary':
                output = self._output_dictionary

            return output

        else:

            raise StopIteration

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if hasattr(self.molecular_system, 'close'):
            self.molecular_system.close()
